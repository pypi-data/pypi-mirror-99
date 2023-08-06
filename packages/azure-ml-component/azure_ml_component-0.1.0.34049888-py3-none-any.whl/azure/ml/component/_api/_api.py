# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json

from typing import List, Mapping, Optional
from concurrent.futures import ThreadPoolExecutor

from msrest import Serializer
from azureml.exceptions import UserErrorException

from azure.ml.component._util._utils import _get_enum
from azure.ml.component._api._api_impl import ModuleAPICaller, ComponentAPICaller
from azure.ml.component._api._component_source import ComponentSource, ComponentSourceParams
from azure.ml.component._api._snapshots_client import SnapshotsClient
from azure.ml.component._api._utils import _write_file_to_local, _download_file_to_local
from azure.ml.component._restclients.designer.models import ParameterType, UIWidgetTypeEnum, \
    StructuredInterfaceParameter, StructuredInterfaceInput, StructuredInterfaceOutput, ModuleEntity, \
    ArgumentAssignment, ArgumentValueType
from azure.ml.component._restclients.designer.models.designer_service_client_enums import SuccessfulCommandReturnCode

definition_cache = {}
pool = ThreadPoolExecutor()


class _DefinitionInterface(dict):
    """This class is used for hard coded converting ModuleDto to ComponentDefinition."""

    DATASET_OUTPUT_PREFIX = 'DatasetOutputConfig:'
    DATASET_OUTPUT_PREFIX_LEN = len(DATASET_OUTPUT_PREFIX)
    PARALLEL_INPUT_PREFIX = '--input_fds_'

    @classmethod
    def get_io_by_dto(cls, dto):
        """Get the inputs/outputs/parameters from a module dto."""

        from azure.ml.component._module_dto import ModuleDto
        if not isinstance(dto, ModuleDto):
            raise ValueError("The input must be ModuleDto.")

        name_argument_name_mapping = dto.module_python_interface.name_mapping
        interface = dto.module_entity.structured_interface
        result = {'inputs': {}, 'outputs': {}}
        name2command = {}

        for input in interface.inputs:
            arg_name = name_argument_name_mapping[input.name]
            result['inputs'][arg_name] = cls.get_input_dict(input)
            name2command[input.name] = '{inputs.%s}' % arg_name

        for output in interface.outputs:
            arg_name = name_argument_name_mapping[output.name]
            result['outputs'][arg_name] = cls.get_output_dict(output)
            name2command[output.name] = '{outputs.%s}' % arg_name

        for param in interface.parameters:
            if param.name not in name_argument_name_mapping:
                continue  # In validate, the returned dto will be runsetting parameters which should be ignored.
            arg_name = name_argument_name_mapping[param.name]
            result['inputs'][arg_name] = cls.get_param_dict(param)
            name2command[param.name] = '{inputs.%s}' % arg_name
        return result, name2command

    @classmethod
    def construct_component_definition_dict_by_dto(cls, dto, basic_info_only=False):
        """Construct the component definition dict according to a module dto."""

        from azure.ml.component._core._component_definition import ComponentType
        from azure.ml.component._core._component_contexts import CreationContext, RegistrationContext
        from azure.ml.component._module_dto import ModuleDto
        if not isinstance(dto, ModuleDto):
            raise ValueError("The input must be ModuleDto.")
        # The logic is learned from MT C# code, MiddleTier.Utilities.ModuleUtilities.ToCustomModuleEntity
        entity = dto.module_entity
        component_type = ComponentType.get_component_type_by_str(dto.job_type)

        creation_context = CreationContext({
            'registeredBy': dto.registered_by,
            'moduleEntity': {
                'createdDate': Serializer.serialize_iso(entity.created_date.isoformat()) if
                entity.created_date else None,
                'lastModifiedDate': Serializer.serialize_iso(entity.last_modified_date.isoformat()) if
                entity.last_modified_date else None,
            }
        })
        registration_context = RegistrationContext({
            'moduleVersionId': dto.module_version_id,
            'defaultVersion': dto.default_version,
            'versions': None if dto.versions is None else
            [{'version': v.version, 'module_version_id': v.module_version_id} for v in dto.versions],
            'moduleSourceType': dto.module_source_type,
            'moduleScope': dto.module_scope,
            'entityStatus': dto.entity_status,
            'yamlLink': dto.yaml_link,
        })

        result = {
            'name': dto.module_name,
            'type': component_type.value,
            'version': dto.module_version,
            'display_name': dto.display_name,
            'description': entity.description,
            'tags': dto.dict_tags,
            'is_deterministic': entity.is_deterministic,
            'creation_context': creation_context,
            'registration_context': registration_context,
        }
        if basic_info_only:  # We do not parse the dto details if we only need basic info.
            return result

        dct, name2command = cls.get_io_by_dto(dto)
        result.update(dct)

        try:
            run_related_args = cls.resolve_run_related_args(dto, component_type, name2command)
            result.update(run_related_args)
        except Exception:
            pass  # Here we simply ignore the error since it doesn't affect .submit(), only .run() is affected.

        return result

    @classmethod
    def resolve_run_related_args(cls, dto, component_type, name2command):
        from azure.ml.component._core._component_definition import ComponentType
        result = {}
        entity = dto.module_entity
        run_config = json.loads(entity.runconfig) if entity.runconfig else None
        if run_config is not None:
            result['environment'] = cls.get_environment_by_run_config(run_config, dto.os_type)
            result['successful_return_code'] = run_config.get(
                'CommandReturnCodeConfig', {}).get('ReturnCode', SuccessfulCommandReturnCode.zero)
            result['is_command'] = not run_config.get('Script', None) and run_config.get('Command', None)
        interface = entity.structured_interface

        if component_type == ComponentType.ParallelComponent:
            result.update(cls.get_parallel_section_by_args(
                interface.arguments, dto.module_python_interface.name_mapping
            ))
        elif component_type == ComponentType.HDInsightComponent:
            result.update(cls.get_hdi_section_by_entity(entity))
        elif component_type == ComponentType.ScopeComponent:
            result.update(cls.get_scope_section_by_dto(dto.entry))

        command = cls.get_command_by_args(interface.arguments, name2command)
        if command:
            # For the two kinds of component, add invoking code.
            if component_type in {ComponentType.CommandComponent, ComponentType.DistributedComponent}:
                # "Command" in run_config indicates that this is an AnyCommand, which uses the first value as the call
                if 'Command' in run_config:
                    command = run_config['Command'].split()[:1] + command
                # Otherwise it is a normal python command, which uses "Script" as the python script.
                else:
                    command = ['python', run_config['Script']] + command
            # For the parallel and scope component, we need to hard-code some command conversion logic.
            elif component_type is ComponentType.ParallelComponent:
                command = cls.update_parallel_command(command, name2command)
            elif component_type is ComponentType.ScopeComponent:
                command = cls.correct_scope_command(interface.arguments, name2command)

            command_str = ' '.join(command)
            if component_type is ComponentType.ParallelComponent:
                # For parallel component, this command is used as parallel.args
                if command_str:
                    result['parallel']['args'] = command_str
            elif component_type is ComponentType.HDInsightComponent:
                # For hdi component, this command is used as hdinsight.args
                if command_str:
                    result['hdinsight']['args'] = command_str
            elif component_type is ComponentType.DistributedComponent:
                # Currently we have only mpi
                result['launcher'] = {'type': 'mpi', 'additional_arguments': command_str}
            elif component_type is ComponentType.ScopeComponent:
                if command_str:
                    result['scope']['args'] = command_str
            else:
                result['command'] = command_str
        return result

    @classmethod
    def get_hdi_section_by_entity(cls, entity: ModuleEntity):
        """For an HDI component, get the HDI related fields."""
        hdi_run_config = entity.cloud_settings.hdi_run_config
        hdinsight_dict = {
            'file': hdi_run_config.file,
            'files': hdi_run_config.files,
            'jars': hdi_run_config.jars,
            'class_name': hdi_run_config.class_name,
            'py_files': hdi_run_config.py_files,
            'archives': hdi_run_config.archives
        }
        # remove empty values
        hdinsight_dict = {key: val for key, val in hdinsight_dict.items() if val}
        return {
            'hdinsight': hdinsight_dict
        }

    @classmethod
    def update_parallel_command(cls, command: List, name2command: Mapping[str, dict]):
        """Update parallel command to be the correct values."""
        # This is a hard-code to remove the arguments used for parallel run driver.
        left_key = '[--process_count_per_node aml_process_count_per_node]'
        left = command.index(left_key) if left_key in command else 0
        right_key = cls.PARALLEL_INPUT_PREFIX + '0'
        right = command.index(right_key) if right_key in command else len(command)
        command = command[left + 1:right]

        for i in range(len(command)):
            arg = command[i]
            if not isinstance(arg, str):
                continue

            if arg.startswith(cls.DATASET_OUTPUT_PREFIX):
                # Change DatasetOutputConfig:xxx to {$outputPath: xxx}
                command[i] = name2command[arg[cls.DATASET_OUTPUT_PREFIX_LEN:]]

        return command

    @classmethod
    def correct_scope_command(cls, args, name2command: Mapping[str, dict]):
        """
        Correct scope command to be the correct values.
        For example when,
        args: [
            (value: 'RawData', value_type: 0),
            (value: 'Text_Data', value_type: 2),
            (value: 'ExtractClause', value_type: 0),
            (value: 'ExtractionClause', value_type: 1),
            (value: 'SS_Data', value_type: 0),
            (value: 'SSPath', value_type: 3)]
        name2command: {
            'RawData': '{inputs.TextData}',
            'SS_Data': '{outputs.SSPath}',
            'PARAM_ExtractClause': '{inputs.ExtractionClause}'}
        Then we get,
        command: [
            'RawData', '{inputs.TextData},
            'ExtractClause', '{inputs.ExtractionClause}',
            'SS_Data', '{outputs.SSPath}']
        """
        command = []
        for arg in args:
            if arg is None:
                continue
            if arg.nested_argument_list:
                # A nested argument list contains another list of ArgumentAssignment,
                # we recursively call the method to get the commands.
                command.append(cls.correct_scope_command(arg.nested_argument_list, name2command))
            elif arg.value_type == '0':  # Just a string value
                command.append(arg.value)
                if arg.value in name2command:
                    command.append(name2command[arg.value])
                # for scope component, MT will add 'PARAM_' as parameter prefix
                elif 'PARAM_' + arg.value in name2command:
                    command.append(name2command['PARAM_' + arg.value])
        return command

    @classmethod
    def get_parallel_section_by_args(cls, args, name_mapping):
        """For a parallel component, get the hdinsight related fields."""

        def get_next_value(target_value) -> Optional[str]:
            """For a command line ['--output', 'xx'], get the value 'xx'."""
            for i in range(len(args) - 1):
                if args[i].value == target_value:
                    return args[i + 1].value
            return None

        output_name = get_next_value('--output')
        if output_name.startswith(cls.DATASET_OUTPUT_PREFIX):
            output_name = output_name[cls.DATASET_OUTPUT_PREFIX_LEN:]
        output_name = name_mapping[output_name]

        result = {
            'parallel': {
                'output_data': output_name,
                'entry': get_next_value('--scoring_module_name'),
            }
        }

        input_data = [get_next_value('%s%d' % (cls.PARALLEL_INPUT_PREFIX, i)) for i in range(len(args))]
        input_data = [name_mapping[value] for value in input_data if value is not None]
        if not input_data:
            return result
        result['parallel']['input_data'] = input_data[0] if len(input_data) == 1 else input_data
        return result

    @classmethod
    def get_scope_section_by_dto(cls, entry_script: str):
        """For scope component, get the scope related fields."""
        scope_dict = {'script': entry_script}
        return {'scope': scope_dict}

    @classmethod
    def get_command_by_args(cls, args: List[ArgumentAssignment], name2command: Mapping[str, dict]):
        """Get the commands according to the arguments in the ModuleDto."""

        # The logic here should align to
        # https://msasg.visualstudio.com/Bing_and_IPG/_git/Aether?path=
        # %2Fsrc%2Faether%2Fplatform%2FbackendV2%2FCloud%2FCommon%2FCloudCommon%2FStructuredInterfaceParserHelper.cs
        # &version=GBmaster&line=153&lineEnd=157&lineStartColumn=1&lineEndColumn=31&lineStyle=plain&_a=contents
        # Currently we divide the logic to two steps,
        # 1 We construct a command string in yaml spec style here;
        # 2 Fill the real value when using component.run
        # TODO: Consider combining the logic of two steps when we actually calling component.run
        # TODO: to make the logic more similar to Pipeline/ES implementation
        command = []
        for arg in args:
            if arg is None:
                continue

            value_type = _get_enum(arg.value_type, ArgumentValueType)

            if value_type == ArgumentValueType.nested_list:
                # A nested argument list contains another list of ArgumentAssignment,
                # we recursively call the method to get the commands, then put "[]" on the two sides.
                optional_arg = '[%s]' % ' '.join(cls.get_command_by_args(arg.nested_argument_list, name2command))
                command.append(optional_arg)
            elif value_type == ArgumentValueType.string_interpolation_list:
                # A string interpolation argument list is a list of ArgumentAssignment which needs to be joined.
                sub_command = cls.get_command_by_args(arg.string_interpolation_argument_list, name2command)
                command.append(''.join(sub_command))
            elif value_type == ArgumentValueType.literal:  # Just a string value
                command.append(arg.value)
            elif value_type in {ArgumentValueType.parameter, ArgumentValueType.input, ArgumentValueType.output}:
                command.append(name2command.get(arg.value, arg.value))
            else:
                raise ValueError("Got unexpected ArgumentAssignment value %s" % arg.value_type)
        return command

    @classmethod
    def get_environment_by_run_config(cls, run_config: dict, os_type: str):
        """Get the environment section according to the run config dict in the module dto."""

        env_in_runconfig = run_config.get('Environment', {})
        dependencies = env_in_runconfig.get('Python', {}).get('CondaDependencies')
        return {
            'name': env_in_runconfig.get('Name', None),
            'version': env_in_runconfig.get('Version', None),
            'conda': {'conda_dependencies': dependencies} if dependencies else None,
            'docker': {'image': env_in_runconfig.get('Docker', {}).get('BaseImage')},
            'os': os_type,
        }

    @classmethod
    def get_param_dict(cls, param: StructuredInterfaceParameter):
        """Get a parameter dict according to the param in the structured interface."""

        from azure.ml.component._core._io_definition import ParameterDefinition
        param_type = _DefinitionInterface._structured_interface_parameter_type(param)
        enum_values = param.enum_values if param.enum_values else None
        return {
            'name': param.name,
            'type': param_type,
            'description': param.description,
            'default': param.default_value,
            # A param which is enabled by another param is also optional.
            'optional': param.is_optional or param.enabled_by_parameter_name is not None,
            'enum': enum_values,
            'min': ParameterDefinition.parse_param(param_type, param.lower_bound, raise_if_fail=False),
            'max': ParameterDefinition.parse_param(param_type, param.upper_bound, raise_if_fail=False),
        }

    @classmethod
    def get_input_dict(cls, input: StructuredInterfaceInput):
        """Get an input dict according to the input in the structured interface."""

        return {
            'name': input.name,
            'type': input.data_type_ids_list[0] if len(input.data_type_ids_list) == 1 else input.data_type_ids_list,
            'optional': input.is_optional,
            'description': input.description,
        }

    @classmethod
    def get_output_dict(cls, output: StructuredInterfaceOutput):
        """Get an output dict according to the output in the structured interface."""

        return {
            'name': output.name,
            'type': output.data_type_id,
            'description': output.description,
        }

    PARAM_NAME_MAPPING = {
        ParameterType.int_enum: 'Integer',
        ParameterType.double: 'Float',
        ParameterType.bool_enum: 'Boolean',
        ParameterType.string: 'String',
        UIWidgetTypeEnum.mode: 'Enum',
        UIWidgetTypeEnum.column_picker: 'ColumnPicker',
        UIWidgetTypeEnum.script: 'Script',
        UIWidgetTypeEnum.credential: 'Credential',
    }

    @staticmethod
    def _structured_interface_parameter_type(param: StructuredInterfaceParameter):
        """Return the type in yaml according to the structured interface parameter."""

        param_type = list(ParameterType)[int(param.parameter_type)]
        ui_type = list(UIWidgetTypeEnum)[int(param.ui_hint.ui_widget_type)] if param.ui_hint else None
        return _DefinitionInterface.PARAM_NAME_MAPPING.get(ui_type) or \
            _DefinitionInterface.PARAM_NAME_MAPPING.get(param_type, 'String')


def _get_dto_hash(dto, workspace):
    """Get hash value of a ModuleDto."""
    # use workspace, namespace, name and version id to calculate hash
    return hash((str(workspace), dto.namespace, dto.module_name, dto.module_version_id))


def _dto_2_definition(dto, workspace=None, basic_info_only=False):
    """Convert from ModuleDto to CommandComponentDefinition.

    :param dto: ModuleDto
    :param workspace: Workspace
    :type dto: azure.ml.component._restclients.designer.models.ModuleDto
    :return: CommandComponentDefinition
    """
    from azure.ml.component._core._component_definition import ComponentType
    from azure.ml.component._core._run_settings_definition import RunSettingsDefinition
    from azure.ml.component._module_dto import ModuleDto

    # Here we use the hash of the dto object as a cache key,
    definition_cache_key = _get_dto_hash(dto, workspace)
    if definition_cache_key in definition_cache:
        return definition_cache[definition_cache_key]

    if not isinstance(dto, ModuleDto):
        dto = ModuleDto(dto)
        dto.correct_module_dto()  # Update some fields to make sure this works well.

    dct = _DefinitionInterface.construct_component_definition_dict_by_dto(dto, basic_info_only=basic_info_only)
    cls = ComponentType.get_component_type_by_str(dct['type']).get_definition_class()
    result = cls._from_dict(dct)

    if not basic_info_only:
        result._runsettings = RunSettingsDefinition.from_dto_runsettings(dto.run_setting_parameters)
    result._workspace = workspace
    result._identifier = dto.module_version_id  # This id is the identifier in the backend server.

    # TODO: Remove the reference to module_dto here.
    result._module_dto = dto
    # Set namespace from dto for backward compatibility in Module SDK
    result._namespace = dto.namespace

    # Put the result in the cache if the component is fully parsed.
    if not basic_info_only:
        definition_cache[definition_cache_key] = result
    return result


class ModuleAPI:
    """CRUD operations for Component.

    Contains some client side logic(Value check, log, etc.)
    Actual CRUD are implemented via CRUDImplementation.
    """

    def __init__(self, workspace, logger, from_cli=False, imp=None):
        """Init component api

        :param workspace: workspace
        :param logger: logger
        :param from_cli: mark if this service caller is used from cli.
        :param imp: api caller implementation
        """
        self.workspace = workspace
        self.logger = logger
        if imp is None:
            imp = ModuleAPICaller(workspace, from_cli)
        self.imp = imp

    def _parse(self, component_source):
        """Parse component source to ModuleDto.

        :param component_source: Local component source.
        :return: ModuleDto
        :rtype: azure.ml.component._restclients.designer.models.ModuleDto
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        with ComponentSourceParams(component_source).create(spec_only=True) as params:
            return self.imp.parse(**params)

    def _validate_component(self, component_source):
        """Validate a component.

        :param component_source: Local component source.
        :return: ModuleDto
        :rtype: azure.ml.component._restclients.designer.models.ModuleDto
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        component_dto = self._parse(component_source)
        entry = component_dto.entry
        if entry and component_source.is_invalid_entry(entry):
            msg = "Entry file '%s' doesn't exist in source directory." % entry
            raise UserErrorException(msg)
        return component_dto

    def register(
            self, spec_file, package_zip: str = None, anonymous_registration: bool = False,
            set_as_default: bool = False, amlignore_file: str = None, version: str = None
    ):
        """Register the component to workspace.

        :param spec_file: The component spec file. Accepts either a local file path, a GitHub url,
                            or a relative path inside the package specified by --package-zip.
        :type spec_file: Union[str, None]
        :param package_zip: The zip package contains the component spec and implementation code.
                            Currently only accepts url to a DevOps build drop.
        :type package_zip: Union[str, None]
        :param anonymous_registration: Whether to register the component as anonymous.
        :type anonymous_registration: bool
        :param set_as_default: Whether to update the default version.
        :type set_as_default: Union[str, None]
        :param amlignore_file: The .amlignore or .gitignore file used to exclude files/directories in the snapshot.
        :type amlignore_file: Union[str, None]
        :param version: If specified, registered component will use specified value as version
                                            instead of the version in the yaml.
        :type version: Union[str, None]
        :return: CommandComponentDefinition
        """
        spec_file = None if spec_file is None else str(spec_file)
        component_source = ComponentSource.from_source(
            spec_file, package_zip, amlignore_file=amlignore_file, logger=self.logger)
        if component_source.is_local_source():
            self._validate_component(component_source)

        register_params = {
            'anonymous_registration': anonymous_registration,
            'validate_only': False,
            'set_as_default': set_as_default,
            'version': version
        }

        with ComponentSourceParams(component_source).create() as params:
            register_params.update(**params)
            component = self.imp.register(**register_params)

        return _dto_2_definition(component, self.workspace)

    def validate(self, spec_file, package_zip):
        """Validate a component.

        :param spec_file: The component spec file. Accepts either a local file path, a GitHub url,
                            or a relative path inside the package specified by --package-zip.
        :type spec_file: str
        :param package_zip: The zip package contains the component spec and implementation code.
                            Currently only accepts url to a DevOps build drop.
        :type package_zip: str
        :return: CommandComponentDefinition
        """
        component_source = ComponentSource.from_source(spec_file, package_zip, logger=self.logger)
        component = self._validate_component(component_source)
        return _dto_2_definition(component, self.workspace, basic_info_only=True)

    def list(self, include_disabled=False, continuation_header=None):
        """Return a list of components in the workspace.

        :param include_disabled: Include disabled components in list result
        :param continuation_header: When not all components are returned, use this to list again.
        :return: A list of CommandComponentDefinition.
        :rtype: builtin.list[CommandComponentDefinition]
        """
        paginated_component = self.imp.list(include_disabled=include_disabled, continuation_header=continuation_header)

        components = paginated_component.value
        component_definitions = []
        for component in components:
            component_definitions.append(_dto_2_definition(component, self.workspace, basic_info_only=True))

        if paginated_component.continuation_token:
            continuation_header = {'continuationToken': paginated_component.continuation_token}
            component_definitions += self.list(
                include_disabled=include_disabled,
                continuation_header=continuation_header
            )
        return component_definitions

    def get(self, name, namespace, version=None):
        """Return the component object.

        :param name: The name of the component to return.
        :type name: str
        :param namespace: The namespace of the component to return.
        :type namespace: str
        :param version: The version of the component to return.
        :type version: str
        :return: CommandComponentDefinition
        """
        component = self.imp.get(name=name, namespace=namespace, version=version)
        return _dto_2_definition(component, self.workspace)

    def get_by_id(self, _id):
        """Return the component object.

        :param id: The id of the component to return.
        :type id: str
        """
        component = self.imp.get_by_id(_id=_id)
        return _dto_2_definition(component, self.workspace)

    def batch_get(self, module_version_ids, name_identifiers):
        """Batch get component objects.

        :param module_version_ids:
        :type module_version_ids: list
        :param name_identifiers:
        :type name_identifiers: list
        """
        result = self.imp.batch_get(module_version_ids, name_identifiers)
        return [_dto_2_definition(dto, self.workspace) for dto in result]

    def enable(self, name, namespace):
        """Enable a component.

        :param name: The name of the component.
        :type name: str
        :param namespace: The namespace of the component.
        :type namespace: str
        :return: CommandComponentDefinition
        """
        component = self.imp.enable(name=name, namespace=namespace)
        return _dto_2_definition(component, self.workspace)

    def disable(self, name, namespace):
        """Disable a component.

        :param name: The name of the component.
        :type name: str
        :param namespace: The namespace of the component.
        :type namespace: str
        :return: CommandComponentDefinition
        """
        component = self.imp.disable(name=name, namespace=namespace)
        return _dto_2_definition(component, self.workspace)

    def set_default_version(self, name, namespace, version):
        """Set a component's default version.

        :param name: The name of the component.
        :type name: str
        :param version: The version to be set as default.
        :type name: str
        :param namespace: The namespace of the component.
        :type namespace: str
        :return: CommandComponentDefinition
        """
        component = self.imp.set_default_version(name=name, namespace=namespace, version=version)
        return _dto_2_definition(component, self.workspace)

    def download(self, name, namespace, version, target_dir, overwrite, include_component_spec=True):
        """Download a component to a local folder.

        :param name: The name of the component.
        :type name: str
        :param namespace: The namespace of the component.
        :type name: str
        :param version: The version of the component.
        :type version: str
        :param target_dir: The directory which you download to.
        :type version: str
        :param overwrite: Set true to overwrite any exist files, otherwise false.
        :type overwrite: bool
        :param include_component_spec: Set true to download component spec file along with the snapshot.
        :type include_component_spec: bool
        :return: The component file path.
        :rtype: dict
        """
        base_filename = "{0}-{1}-{2}-{3}".format(
            self.imp._workspace.service_context.workspace_name,
            name,
            namespace,
            version or 'default',
        )

        file_path = {}

        if include_component_spec:
            # download component spec
            module_yaml = self.get_module_yaml(name, namespace, version)
            module_spec_file_name = _write_file_to_local(module_yaml, target_dir=target_dir,
                                                         file_name=base_filename + ".yaml", overwrite=overwrite,
                                                         logger=self.logger)
            file_path['module_spec'] = module_spec_file_name

        # download snapshot
        snapshot_url = self.get_snapshot_url(name, namespace, version)
        snapshot_filename = _download_file_to_local(snapshot_url, target_dir=target_dir,
                                                    file_name=base_filename + ".zip", overwrite=overwrite,
                                                    logger=self.logger)
        file_path['snapshot'] = snapshot_filename
        return file_path

    def get_module_yaml(self, name, namespace, version):
        """Get component yaml of component.

        :param name: The name of the component.
        :type name: str
        :param version: The version to be set as default.
        :type name: str
        :param namespace: The namespace of the component.
        :type namespace: str
        :return: yaml content
        """
        yaml = self.imp.get_module_yaml(name=name, namespace=namespace, version=version)
        return yaml

    def get_snapshot_url(self, name, namespace, version):
        """Get a component snapshot download url.

        :param name: The name of the component.
        :type name: str
        :param namespace: The namespace of the component.
        :type namespace: str
        :param version: The version of the component.
        :type version: str
        :return: The component snapshot url.
        """
        snapshot_url = self.imp.get_snapshot_url(name=name, namespace=namespace, version=version)
        return snapshot_url

    def get_snapshot_url_by_id(self, component_id):
        """Get a component snapshot download url by id.

        :param component_id: component version id
        :return: The component snapshot url.
        """
        snapshot_url = self.imp.get_snapshot_url_by_id(component_id=component_id)
        return snapshot_url


class ComponentAPI(ModuleAPI):
    """CRUD operations for Component.

    Contains some client side logic(Value check, log, etc.)
    Actual CRUD are implemented via CRUDImplementation.
    """

    def __init__(self, workspace, logger, from_cli=False):
        """Init component api

        :param workspace: workspace
        :param logger: logger
        :param from_cli: mark if this service caller is used from cli.
        """
        self.workspace = workspace
        self.imp = ComponentAPICaller(workspace, from_cli)
        self.moduleImp = ModuleAPICaller(workspace, from_cli)
        self.logger = logger

    def get(self, name, version=None):
        """Return the component object.

        :param name: The name of the component to return.
        :type name: str
        :param version: The version of the component to return.
        :type version: str
        :return: CommandComponentDefinition
        """
        component = self.imp.get(name=name, version=version)
        return _dto_2_definition(component, self.workspace)

    def enable(self, name):
        """Enable a component.

        :param name: The name of the component.
        :type name: str
        :return: CommandComponentDefinition
        """
        component = self.imp.enable(name=name)
        return _dto_2_definition(component, self.workspace)

    def disable(self, name):
        """Disable a component.

        :param name: The name of the component.
        :type name: str
        :return: CommandComponentDefinition
        """
        component = self.imp.disable(name=name)
        return _dto_2_definition(component, self.workspace)

    def set_default_version(self, name, version):
        """Set a component's default version.

        :param name: The name of the component.
        :type name: str
        :param version: The version to be set as default.
        :type version: str
        :return: CommandComponentDefinition
        """
        component = self.imp.set_default_version(name=name, version=version)
        return _dto_2_definition(component, self.workspace)

    def download(self, name, version, target_dir, overwrite, include_component_spec=True):
        """Download a component to a local folder.

        :param name: The name of the component.
        :type name: str
        :param version: The version of the component.
        :type version: str
        :param target_dir: The directory which you download to.
        :type version: str
        :param overwrite: Set true to overwrite any exist files, otherwise false.
        :type overwrite: bool
        :param include_component_spec: Set true to download component spec file along with the snapshot.
        :type include_component_spec: bool
        :return: The component file path.
        :rtype: dict
        """
        base_filename = "{0}-{1}-{2}".format(
            self.imp._workspace.service_context.workspace_name,
            name,
            version or 'default',
        )

        file_path = {}

        if include_component_spec:
            # download component spec
            module_yaml = self.get_module_yaml(name, version)
            module_spec_file_name = _write_file_to_local(module_yaml, target_dir=target_dir,
                                                         file_name=base_filename + ".yaml", overwrite=overwrite,
                                                         logger=self.logger)
            file_path['component_spec'] = module_spec_file_name

        # download snapshot
        snapshot_url = self.get_snapshot_url(name, version)
        snapshot_filename = _download_file_to_local(snapshot_url, target_dir=target_dir,
                                                    file_name=base_filename + ".zip", overwrite=overwrite,
                                                    logger=self.logger)
        file_path['snapshot'] = snapshot_filename
        return file_path

    def get_module_yaml(self, name, version):
        """Get component yaml of component.

        :param name: The name of the component.
        :type name: str
        :param version: The version to be set as default.
        :type version: str
        :return: yaml content
        """
        yaml = self.imp.get_module_yaml(name=name, version=version)
        return yaml

    def get_snapshot_url(self, name, version):
        """Get a component snapshot download url.

        :param name: The name of the component.
        :type name: str
        :param version: The version of the component.
        :type version: str
        :return: The component snapshot url.
        """
        snapshot_url = self.imp.get_snapshot_url(name=name, version=version)
        return snapshot_url

    def get_snapshot_url_by_id(self, component_id):
        """Get a component snapshot download url by id.

        :param component_id: component version id
        :return: The component snapshot url.
        """
        snapshot_url = self.moduleImp.get_snapshot_url_by_id(component_id=component_id)
        return snapshot_url

    def get_versions(self, component_name):
        """Get all versions of a component.

        :param component_name: The name of the component
        :return: A list of CommandComponentDefinition.
        :rtype: builtin.dict[str, CommandComponentDefinition]
        """
        return {version: _dto_2_definition(dto, self.workspace) for version, dto in
                self.imp.get_versions(name=component_name).items()}

    def register(
            self, spec_file, package_zip: str = None, anonymous_registration: bool = False,
            set_as_default: bool = False, amlignore_file: str = None, version: str = None
    ):
        """Register the component to workspace.

        :param spec_file: The component spec file. Accepts either a local file path, a GitHub url,
                            or a relative path inside the package specified by --package-zip.
        :type spec_file: Union[str, None]
        :param package_zip: The zip package contains the component spec and implementation code.
                            Currently only accepts url to a DevOps build drop.
        :type package_zip: Union[str, None]
        :param anonymous_registration: Whether to register the component as anonymous.
        :type anonymous_registration: bool
        :param set_as_default: Whether to update the default version.
        :type set_as_default: Union[str, None]
        :param amlignore_file: The .amlignore or .gitignore file used to exclude files/directories in the snapshot.
        :type amlignore_file: Union[str, None]
        :param version: If specified, registered component will use specified value as version
                                            instead of the version in the yaml.
        :type version: Union[str, None]
        :return: CommandComponentDefinition
        """
        spec_file = None if spec_file is None else str(spec_file)
        component_source = ComponentSource.from_source(
            spec_file, package_zip, amlignore_file=amlignore_file, logger=self.logger)
        snapshot_id = None
        if component_source.is_local_source():
            # Create snapshot task. Since creating snapshot is almost an IO job as validating component,
            # so we do it in another thread to save time
            snapshot_task = pool.submit(
                create_snapshot, component_source.snapshot, self.workspace)
            component_dto = self._validate_component(component_source)
            # For local yaml, we create snapshot on client side, and pass entry and yaml files to MT
            # Instead of parsing entry from yaml our own, we choose to get it from the validation result
            # So we set it here
            component_source.snapshot.entry_file_relative_path = component_dto.entry
            # Note: we call snapshot_task.get() at last, so if both create_snapshot and validate has exceptions,
            # only exceptions in validate will be raised.
            # Get snapshot id
            snapshot_id = snapshot_task.result()

        register_params = {
            'anonymous_registration': anonymous_registration,
            'validate_only': False,
            'set_as_default': set_as_default,
            'version': version,
            'snapshot_id': snapshot_id
        }

        with ComponentSourceParams(component_source).create(spec_only=(snapshot_id is not None)) as params:
            register_params.update(**params)
            component = self.imp.register(**register_params)

        return _dto_2_definition(component, self.workspace)


def create_snapshot(snapshot, workspace):
    snapshot_folder = snapshot._get_snapshot_folder()
    snapshots_client = SnapshotsClient(workspace, logger=snapshot.logger)
    return snapshots_client.create_snapshot(
        snapshot_folder, snapshot.total_size, component_file=snapshot._spec_file_path)
