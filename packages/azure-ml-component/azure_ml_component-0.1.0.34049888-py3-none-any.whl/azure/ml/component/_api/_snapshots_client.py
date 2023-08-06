# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import json
from uuid import UUID

from azure.ml.component._util._loggerfactory import track, _LoggerFactory
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin
from azure.ml.component._util._utils import TimerContext
from azureml._restclient.snapshots_client import SnapshotsClient as BaseSnapshotsClient
from azureml._base_sdk_common.merkle_tree import DirTreeJsonEncoder, create_merkletree, DirTreeNode
from azureml._base_sdk_common.merkle_tree_differ import compute_diff
from azureml.exceptions import SnapshotException
from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._base_sdk_common.utils import create_session_with_retry
from azureml._base_sdk_common.common import get_http_exception_response_string
from azureml._base_sdk_common.snapshot_dto import SnapshotDto
from ._snapshot_cache import SnapshotCache
from .._aml_core_dependencies import SNAPSHOT_MAX_FILES, SNAPSHOT_BATCH_SIZE, ONE_MB, SNAPSHOT_MAX_SIZE_BYTES

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class SnapshotsClient(BaseSnapshotsClient, WorkspaceTelemetryMixin):
    """
    Snapshot client class, extended from azureml._restclient.snapshots_client.SnapshotsClient.
    Add snapshot cache per component.

    :param workspace: Workspace for this client
    :type workspace: azureml.core.Workspace
    :param logger: the logger used to log info and warning happened during uploading snapshot
    :type logger: logging.Logger
    """
    def __init__(self, workspace, logger=None):
        # the mro of this class is BaseSnapshotsClient -> WorkspaceClient -> ClientBase -> ChainedIdentity
        # -> WorkspaceTelemetryMixin -> TelemetryMixin -> object
        super(SnapshotsClient, self).__init__(workspace.service_context, workspace=workspace)
        self._cache = SnapshotCache(self._service_context)
        if not logger:
            self.logger = logging.getLogger('snapshot')
        else:
            self.logger = logger

    def validate_snapshot_size(self, size, component_file, raise_on_validation_failure):
        """Validate size of snapshot.

        :param size: Size of component snapshot.
        :param component_file: The component spec file.
        :param raise_on_validation_failure: Raise error if validation failed.
        """
        if size > SNAPSHOT_MAX_SIZE_BYTES:
            error_message = "====================================================================\n" \
                            "\n" \
                            "While attempting to take snapshot of {}\n" \
                            "Your total snapshot size exceeds the limit of {} MB.\n" \
                            "Please see http://aka.ms/aml-largefiles on how to work with large files.\n" \
                            "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug " \
                            "the creating process of component snapshots.\n" \
                            "\n" \
                            "====================================================================\n" \
                            "\n".format(component_file, SNAPSHOT_MAX_SIZE_BYTES / ONE_MB)
            if raise_on_validation_failure:
                raise SnapshotException(error_message)
            else:
                self.logger.warning(error_message)

    @track(_get_logger)
    def create_snapshot(
            self, snapshot_folder, size,
            component_file=None, retry_on_failure=True, raise_on_validation_failure=True):
        """Create snapshot on given merkle tree root and snapshot size.
        support cache and incrementally update based on latest snapshot

        :param component_file: Component base folder, used to calculate cache file location
        :param snapshot_folder: Snapshot base folder.
        :param size: snapshot size
        :param retry_on_failure:
        :param raise_on_validation_failure:
        :return:
        """
        if component_file is None:
            component_file = snapshot_folder

        # add extra dimensions(eg: snapshot size, upload time) to logger
        track_dimensions = {}

        auth_headers = self.auth.get_authentication_header()

        self.validate_snapshot_size(size, component_file, raise_on_validation_failure)

        # Get the previous snapshot for this project
        parent_root, parent_snapshot_id = self._cache.get_latest_snapshot_by_path(component_file)

        # Compute the dir tree for the current working set
        # The folder passed here has already excluded ignored files, so we do not need to check that
        def _is_file_excluded(file):
            return False
        curr_root = create_merkletree(snapshot_folder, _is_file_excluded)

        # Compute the diff between the two dirTrees
        entries = compute_diff(parent_root, curr_root)

        # If there are no changes, just return the previous snapshot_id
        if not len(entries):
            self.logger.info("The snapshot did not change compared to local cached one, reused local cached snapshot.")
            track_dimensions.update({'local_cache': True})
            _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
            return parent_snapshot_id

        # get new snapshot id by snapshot hash
        snapshot_id = str(UUID(curr_root.hexdigest_hash[::4]))
        track_dimensions.update({'snapshot_id': snapshot_id})

        # Check whether the snapshot with new id already exists
        snapshot_dto = self.get_snapshot_metadata_by_id(snapshot_id)
        if snapshot_dto is None:
            entries_to_send = [entry for entry in entries if (
                entry.operation_type == 'added' or entry.operation_type == 'modified') and entry.is_file]
            if len(entries_to_send) > SNAPSHOT_MAX_FILES and not os.environ.get("AML_SNAPSHOT_NO_FILE_LIMIT"):
                error_message = "====================================================================\n" \
                                "\n" \
                                "While attempting to take snapshot of {}\n" \
                                "Your project exceeds the file limit of {}.\n" \
                                "Please see http://aka.ms/troubleshooting-code-snapshot on how to debug " \
                                "the creating process of component snapshots.\n" \
                                "\n" \
                                "====================================================================\n" \
                                "\n".format(component_file, SNAPSHOT_MAX_FILES)
                if raise_on_validation_failure:
                    raise SnapshotException(error_message)
                else:
                    self.logger.warning(error_message)

            custom_headers = {
                "dirTreeRootFile": "true"
            }

            dir_tree_file_contents = json.dumps(curr_root, cls=DirTreeJsonEncoder)

            # Git metadata
            snapshot_properties = global_tracking_info_registry.gather_all(snapshot_folder)

            with create_session_with_retry() as session:

                # There is an OS limit on how many files can be open at once, so we \
                # must batch the snapshot to not exceed the limit.
                # We take multiple snapshots, each building on each other, and return the final snapshot.
                new_snapshot_id = None
                # We always need to do at least one pass,
                # for the case where the only change is deleted files in dirTreeRootFile
                first_pass = True
                while len(entries_to_send) or first_pass:
                    first_pass = False
                    files_to_send = []
                    files_to_close = []
                    if new_snapshot_id:
                        # If updated files count >= 2000, we will get a new snapshot id
                        parent_snapshot_id = new_snapshot_id
                    new_snapshot_id = snapshot_id
                    self.logger.info(
                        "Collecting snapshot files to upload, only added or modified files will be uploaded.")
                    try:
                        total_size = 0
                        with TimerContext() as timer_context:
                            # Add entries until we hit batch limit
                            while len(files_to_send) < SNAPSHOT_BATCH_SIZE and len(entries_to_send):
                                entry = entries_to_send.pop()
                                path_env = (os.path.join(snapshot_folder, entry.node_path)
                                            if os.path.isdir(snapshot_folder)
                                            else entry.node_path)
                                file_obj = open(path_env, "rb")
                                files_to_send.append(("files", (entry.node_path, file_obj)))
                                files_to_close.append(file_obj)
                                total_size += os.path.getsize(path_env)
                                self.logger.info("\t{} {}".format(
                                    str(entry.operation_type).capitalize(), entry.node_path))
                            collect_duration_seconds = timer_context.get_duration_seconds()
                            total_size = total_size / 1024
                            track_dimensions.update({
                                'files_to_send': len(files_to_send),
                                'collect_duration_seconds': collect_duration_seconds,
                                'total_size': total_size
                            })
                            self.logger.info(
                                'Collected {} files to upload in {:.2f} seconds, total size {:.2f} KB'.format(
                                    len(files_to_send), collect_duration_seconds, total_size))
                        # directory_tree needs to be added to all snapshot requests
                        files_to_send.append(
                            ("files", ("dirTreeRootFile", dir_tree_file_contents, "application/json", custom_headers)))
                        files_to_send.append(("properties", (None, json.dumps(snapshot_properties))))

                        url = self._service_context._get_project_content_url() + "/content/v1.0" + \
                            self._service_context._get_workspace_scope() + "/snapshots/" + \
                            new_snapshot_id + "?parentSnapshotId=" + parent_snapshot_id

                        # record time spent when uploading snapshot
                        with TimerContext() as timer_context:
                            response = self._execute_with_base_arguments(
                                session.post, url, files=files_to_send, headers=auth_headers)
                            upload_duration_seconds = timer_context.get_duration_seconds()
                            track_dimensions.update({
                                'upload_duration_seconds': upload_duration_seconds
                            })
                            self.logger.info('Uploaded snapshot in {:.2f} seconds.'.format(upload_duration_seconds))

                        if response.status_code >= 400:
                            if retry_on_failure:
                                # The cache may have been corrupted, so clear it and try again.
                                self._cache.remove_latest()
                                return self.create_snapshot(
                                    snapshot_folder, size, component_file, retry_on_failure=False)
                            else:
                                raise SnapshotException(get_http_exception_response_string(response))
                    finally:
                        for f in files_to_close:
                            f.close()

            snapshot_dto = SnapshotDto(dir_tree_file_contents, new_snapshot_id)
        else:
            self.logger.info("Found remote cache of snapshot, reused remote cached snapshot.")
            track_dimensions.update({'workspace_cache': True})
            new_snapshot_id = snapshot_id

        # Update the cache
        self._cache.update_cache(snapshot_dto, component_file)
        # update tracked dimensions
        _LoggerFactory.add_track_dimensions(_get_logger(), track_dimensions)
        return new_snapshot_id

    def get_snapshot_metadata_by_id(self, snapshot_id):
        """
        200 indicates the snapshot with this id exists, 404 indicates not exists
        If other status codes returned, by default we will retry 3 times until we get 200 or 404
        """
        auth_headers = self.auth.get_authentication_header()
        url = self._service_context._get_project_content_url() + "/content/v1.0" + \
            self._service_context._get_workspace_scope() + "/snapshots/" + \
            snapshot_id + "/metadata"
        with create_session_with_retry() as session:
            response = self._execute_with_base_arguments(
                session.get, url, headers=auth_headers)
            if response.status_code == 200:
                response_data = response.content.decode('utf-8')
                snapshot_dict = json.loads(response_data)
                root_dict = snapshot_dict['root']
                snapshot_id = snapshot_dict['id']
                node = DirTreeNode()
                node.load_object_from_dict(root_dict)
                root = json.dumps(node, cls=DirTreeJsonEncoder)
                return SnapshotDto(root, snapshot_id)
            elif response.status_code == 404:
                return None
            else:
                raise SnapshotException(get_http_exception_response_string(response))
