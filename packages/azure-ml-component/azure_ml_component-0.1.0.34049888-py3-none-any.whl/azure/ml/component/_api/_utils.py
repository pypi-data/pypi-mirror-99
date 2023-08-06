# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import re
import shutil
import requests
import zipfile
import posixpath
import ntpath
import hashlib

from pathlib import Path

from azureml.exceptions import UserErrorException

_RE_GITHUB_URL = re.compile(r'^(https://github.com/[\w\-.]+/[\w\-.]+)')
_EMPTY_GUID = '00000000-0000-0000-0000-000000000000'


def _looks_like_a_url(input_str):
    return input_str and (input_str.startswith('http://') or input_str.startswith('https://'))


def _normalize_file_name(target_dir=None, file_name=None, overwrite=False, logger=None):
    """Return a valid full file path to write."""
    if not target_dir:
        target_dir = os.getcwd()
        logger.debug("Target dir is not provided, use cwd: {}".format(target_dir))
    else:
        target_dir = os.path.abspath(target_dir)
        logger.debug("Normalized target dir: {}".format(target_dir))

    target_path = Path(target_dir)
    if not target_path.exists():
        raise ValueError("Target dir does not exist.")

    if target_path.is_file():
        raise ValueError("Target dir is not a directory.")

    if not file_name:
        raise ValueError("File name is required.")

    file_name = _replace_invalid_char_in_file_name(file_name)
    full_file_path = target_path / file_name

    logger.debug("Normalized file name: {}".format(full_file_path))
    if not overwrite and full_file_path.exists():
        raise ValueError("File already exists, use -y if you attempt to overwrite.")

    return str(full_file_path)


def _download_file(url, file_name, logger):
    res = requests.get(url, allow_redirects=True, stream=True)

    logger.debug("Create file: {0}".format(file_name))
    with open(file_name, 'wb') as fp:
        # from document, chunk_size=None will read data as it arrives in whatever size the chunks are received.
        # UPDATED: chunk_size could not be None since it will return the whole content as one chunk only
        #          due to the implementation of urllib3, thus the progress bar could not displayed correctly.
        #          Changed to a chunk size of 1024.
        for buf in res.iter_content(chunk_size=1024):
            fp.write(buf)
    logger.debug("Download complete.")


def _download_file_to_local(url, target_dir=None, file_name=None, overwrite=False, logger=None):
    file_name = _normalize_file_name(target_dir=target_dir, file_name=file_name, overwrite=overwrite, logger=logger)

    # download file
    _download_file(url, file_name, logger)
    return file_name


def _make_zipfile(zip_file_path, folder_or_file_to_zip, exclude_function=None):
    """Create an archive with exclusive files or directories. Adapted from shutil._make_zipfile.

    :param zip_file_path: Path of zip file to create.
    :param folder_or_file_to_zip: Directory or file that will be zipped.
    :param exclude_function: Function of exclude files or directories
    """
    with zipfile.ZipFile(zip_file_path, "w") as zf:
        if os.path.isfile(folder_or_file_to_zip):
            zf.write(folder_or_file_to_zip, os.path.basename(folder_or_file_to_zip))
        else:
            for dirpath, dirnames, filenames in os.walk(folder_or_file_to_zip):
                relative_dirpath = os.path.relpath(dirpath, folder_or_file_to_zip)
                for name in sorted(dirnames):
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    zf.write(full_path, relative_path)
                for name in filenames:
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    if os.path.isfile(full_path):
                        zf.write(full_path, relative_path)


def _replace_invalid_char_in_file_name(file_name, rep='_'):
    """Replace all invalid characters (<>:"/\\|?*) in file name."""
    invalid_file_name_chars = r'<>:"/\|?*'
    return "".join(rep if c in invalid_file_name_chars else c for c in file_name)


def _write_file_to_local(content, target_dir=None, file_name=None, overwrite=False, logger=None):
    file_name = _normalize_file_name(target_dir=target_dir, file_name=file_name, overwrite=overwrite, logger=logger)

    # save file
    with open(file_name, 'w') as fp:
        # we suppose that content only use '\n' as EOL.
        fp.write(content)
    return file_name


def get_value_by_key_path(dct, key_path, default_value=None):
    """Given a dict, get value from key path.

    >>> dct = {
    ...     'Employee': {
    ...         'Profile': {
    ...             'Name': 'Alice',
    ...             'Age': 25,
    ...         }
    ...     }
    ... }
    >>> get_value_by_key_path(dct, 'Employee/Profile/Name')
    'Alice'
    >>> get_value_by_key_path(dct, 'Employee/Profile/Age')
    25
    >>> get_value_by_key_path(dct, 'Employee/Profile')
    {'Name': 'Alice', 'Age': 25}
    """
    if not key_path:
        raise ValueError("key_path must not be empty")

    segments = key_path.split('/')
    final_flag = object()
    segments.append(final_flag)

    walked = []

    cur_obj = dct
    for seg in segments:
        # If current segment is final_flag,
        # the cur_obj is the object that the given key path points to.
        # Simply return it as result.
        if seg is final_flag:
            # return default_value if cur_obj is None
            return default_value if cur_obj is None else cur_obj

        # If still in the middle of key path, when cur_obj is not a dict,
        # will fail to locate the values
        if not isinstance(cur_obj, dict):
            # TODO: maybe add options to raise exceptions here in the future
            return default_value

        # Move to next segment
        cur_obj = cur_obj.get(seg)
        walked.append(seg)

    raise RuntimeError("Should never go here")


def try_to_get_value_from_multiple_key_paths(dct, key_path_list, default_value=None):
    """Same as get_value_by_key_path, but try to get from multiple key paths,
       try the given key paths one by one."""
    for key_path in key_path_list:
        value = get_value_by_key_path(dct, key_path=key_path)
        if value is not None:
            return value
    return default_value


def is_absolute(file_path):
    # Here we don't use Path(file).is_absolute because it can only handle the case in current OS,
    # but in our scenario, we may run this code in Windows, but need to check whether the path is posix absolute.
    return posixpath.isabs(file_path) or ntpath.isabs(file_path)


def get_file_path_hash(file_path):
    """Get hash value of a file path."""
    import hashlib
    h = hashlib.sha256()
    h.update(Path(file_path).resolve().absolute().as_posix().encode('utf-8'))
    return h.hexdigest()


def create_or_cleanup_folder(folder_path):
    """If folder doesn't exist, create one; else, clean it up.

    :param folder_path: The folder to create or clean up
    :raises: Exception
    """
    if os.path.isfile(folder_path) or os.path.islink(folder_path):
        os.unlink(folder_path)
    elif os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def check_spec_file(spec_file) -> Path:
    """Check if spec file is legal, raise error if illegal."""
    path = Path(spec_file).resolve()
    if not path.exists():
        raise UserErrorException('File {0} not found.'.format(spec_file))

    if path.is_dir():
        raise UserErrorException('spec file could not be a folder.')

    if path.suffix != '.yaml' and path.suffix != '.yml':
        raise UserErrorException('Invalid file {0}. Only accepts *.yaml or *.yml files.'.format(spec_file))
    return path


def default_content_hash_calculator(path):
    """This func is derived from src/azureml-pipeline-core/azureml/pipeline/core/_datasource_builder.py"""
    relative_path_list = []
    if os.path.isfile(path):
        relative_path_list.extend(os.path.basename(path))
        path = os.path.dirname(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=True):
            relative_path_list.extend([os.path.relpath(os.path.join(root, name), path) for name in files])
    else:
        raise ValueError("path not found %s" % path)

    if len(relative_path_list) == 0:
        hash = "00000000000000000000000000000000"
    else:
        hasher = hashlib.md5()
        for f in relative_path_list:
            hasher.update(str(f).encode('utf-8'))
            with open(str(os.path.join(path, f)), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
        hash = hasher.hexdigest()
    return hash
