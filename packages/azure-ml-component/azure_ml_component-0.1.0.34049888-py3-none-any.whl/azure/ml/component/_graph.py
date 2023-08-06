# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import uuid
from pathlib import Path
import json

from azureml.core.compute import AmlCompute, ComputeInstance, RemoteCompute, HDInsightCompute
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

from azure.ml.component._util._utils import _get_dataset_def_from_dataset
from azureml.exceptions import UserErrorException

from .component import Component, Input, Output, _get_workspace_default_datastore
from ._module_dto import _python_type_to_type_code
from ._pipeline_parameters import PipelineParameter
from ._dataset import _GlobalDataset
from ._util._loggerfactory import timer

from ._restclients.designer.models import GraphDraftEntity, GraphModuleNode, GraphDatasetNode, \
    GraphEdge, ParameterAssignment, PortInfo, DataSetDefinition, EntityInterface, Parameter, DataPathParameter, \
    OutputSetting, InputSetting, GraphModuleNodeRunSetting, ComputeSetting, RunSettingParameterType, \
    RunSettingUIWidgetTypeEnum, ComputeType, MlcComputeInfo, RunSettingParameterAssignment
from ._parameter_assignment import _ParameterAssignment


DATAFRAMEDIRECTORY = 'DataFrameDirectory'


class _GraphEntityBuilderContext(object):
    def __init__(self, compute_target=None, pipeline_parameters=None, pipeline_regenerate_outputs=None,
                 module_nodes=None, workspace=None, default_datastore=None):
        """
        Init the context needed for graph builder.

        :param compute_target: The compute target.
        :type compute_target: tuple(name, type)
        :param pipeline_parameters: The pipeline parameters.
        :type pipeline_parameters: dict
        :param pipeline_regenerate_outputs: the `regenerate_output` value of all module node
        :type pipeline_regenerate_outputs: bool
        """
        self.compute_target = compute_target
        # Copy pipeline parameters here because after build graph, dataset parameters will be removed.
        self.pipeline_parameters = {} if pipeline_parameters is None else {**pipeline_parameters}
        self.pipeline_regenerate_outputs = pipeline_regenerate_outputs

        self.module_nodes = module_nodes
        self.workspace = workspace
        # Correct top pipeline's default datastore here.
        if default_datastore is None:
            default_datastore = _get_workspace_default_datastore(workspace)
        self.default_datastore = default_datastore


class _GraphEntityBuilder(object):
    """The builder that constructs SMT graph-related entities from `azure.ml.component.Component`."""
    DATASOURCE_PORT_NAME = 'data'
    DATASOURCE_TYPES = (
        AbstractDataset, DatasetConsumptionConfig, _GlobalDataset, DataReference,
        PipelineParameter,  # Special data source
        str, Path,  # For local run
    )

    def __init__(self, context: _GraphEntityBuilderContext):
        self._context = context
        self._modules = context.module_nodes
        self._nodes = {}
        self._input_nodes = {}
        self._data_path_parameter_input = {}
        self._dataset_parameter_keys = set()
        # This is a mapping from the instance ids of modules(components) in the pipeline
        # to the graph node ids in the built graph.
        # We use this mapping to get the graph node according to the module instance in the pipeline
        # when constructing subpipeline, visualization graph, etc..
        self._module_node_to_graph_node_mapping = {}

    @property
    def module_node_to_graph_node_mapping(self):
        return self._module_node_to_graph_node_mapping

    def _get_node_by_component(self, component: Component):
        return self._nodes.get(self.module_node_to_graph_node_mapping.get(component._get_instance_id()))

    @timer()
    def build_graph_entity(self):
        """
        Build graph entity that can be used to create pipeline draft and pipeline run.

        Notice that context.pipeline_parameters will be modified after build,
            dataset parameters will be removed.
        :return Tuple of (graph entity, module node run settings, dataset definition value assignments)
        :rtype tuple
        """

        graph_entity = GraphDraftEntity()
        self._module_node_to_graph_node_mapping = {}

        # Prepare the entity
        graph_entity.dataset_nodes = []
        graph_entity.module_nodes = []
        graph_entity.edges = []
        graph_entity.entity_interface = EntityInterface(parameters=[], data_path_parameters=[],
                                                        data_path_parameter_list=[])

        if self._context.compute_target is not None:
            default_compute_name, default_compute_type = self._context.compute_target
            graph_entity.default_compute = ComputeSetting(name=default_compute_name,
                                                          compute_type=ComputeType.mlc,
                                                          mlc_compute_info=MlcComputeInfo(
                                                              mlc_compute_type=default_compute_type))

        module_node_run_settings = []

        # Note that we need to generate all module nodes before constructing edges.
        for module in self._modules:
            module_node = self._build_graph_module_node(module, self._context.pipeline_regenerate_outputs)
            graph_entity.module_nodes.append(module_node)
            self._nodes[module_node.id] = module_node

        # Start generating edges and other settings
        for module in self._modules:
            module_node = self._get_node_by_component(module)
            # Note that for old components(especially for built-in components),
            # input_name could be different from argument name, we need to use input_name as the key
            inputs_map = {
                module._get_input_name_by_argument_name(k): i for k, i in module.inputs.items() if i._dset is not None
            }
            for input_name, i in inputs_map.items():
                input_dataset = i._get_internal_data_source()
                if isinstance(input_dataset, self.DATASOURCE_TYPES):
                    dataset_node = self._get_or_create_dataset_node(graph_entity, i)
                    edge = self._produce_edge_dataset_node_to_module_node(input_name, dataset_node, module_node)
                elif isinstance(input_dataset, Output):
                    edge = self._produce_edge_module_node_to_module_node(input_name, input_dataset, module_node)
                else:
                    raise ValueError("Invalid input type: {0}".format(type(input_dataset)))
                if edge is not None:
                    graph_entity.edges.append(edge)

            module_node_run_settings.append(
                self._produce_module_runsettings(module, module_node))

            self._update_module_node_params(graph_entity, module_node, module)

        self._update_data_path_parameter_list(graph_entity)
        # Set this for further usage including creating subpipeline info, creating visualization graph and export.
        # This is a little hacky, but graph_entity is a swagger generated class which cannot be modified,
        # so currently we just keep this.
        setattr(graph_entity, 'module_node_to_graph_node_mapping', self.module_node_to_graph_node_mapping)

        remove_node_ids = self.resolve_empty_nodes(graph_entity)
        graph_entity.dataset_nodes = [node for node in graph_entity.dataset_nodes
                                      if node.id not in remove_node_ids]
        graph_entity.edges = [edge for edge in graph_entity.edges
                              if edge.source_output_port.node_id not in remove_node_ids]
        # Keep graph data path parameter order as original pipeline parameter order.
        graph_entity.entity_interface.data_path_parameter_list = \
            self.sort_parameter_order(graph_entity.entity_interface.data_path_parameter_list)
        graph_entity.entity_interface.parameters = \
            self.sort_parameter_order(graph_entity.entity_interface.parameters)

        return graph_entity, module_node_run_settings

    def build_graph_json(self):
        """Build graph and convert the object to json string recursively."""
        def serialize_object_to_dict(obj):
            if type(obj) in [str, int, float, bool] or obj is None:
                return obj

            if isinstance(obj, dict):
                for k, v in obj.items():
                    obj[k] = serialize_object_to_dict(v)
            elif isinstance(obj, list):
                obj = [serialize_object_to_dict(i) for i in obj]
            else:
                obj = serialize_object_to_dict(obj.__dict__)
            return obj

        import json

        graph, module_node_run_settings = self.build_graph_entity()
        compute_name = None if graph.default_compute is None else graph.default_compute.name
        datastore_name = None if graph.default_datastore is None else graph.default_datastore.data_store_name
        graph_dict = {'module_nodes': [serialize_object_to_dict(i) for i in graph.module_nodes],
                      'dataset_nodes': [serialize_object_to_dict(i) for i in graph.dataset_nodes],
                      'edges': [serialize_object_to_dict(i) for i in graph.edges],
                      'entity_interface': serialize_object_to_dict(graph.entity_interface),
                      'default_compute': compute_name,
                      'default_datastore': datastore_name,
                      'module_node_run_settings': serialize_object_to_dict(module_node_run_settings)}

        return json.dumps(graph_dict, indent=4, sort_keys=True)

    def sort_parameter_order(self, parameters_list):
        parameters = {_p.name: _p for _p in parameters_list}
        results = {_k: parameters[_k] for _k in self._context.pipeline_parameters.keys() if _k in parameters}
        results.update({_p.name: _p for _p in parameters_list if _p.name not in results})
        return list(results.values())

    def resolve_empty_nodes(self, graph_entity):
        remove_node_ids = []
        data_path_param_names = set(i.name for i in graph_entity.entity_interface.data_path_parameter_list
                                    if i.default_value is not None)
        for node in graph_entity.dataset_nodes:
            dataset_def = node.data_set_definition
            if dataset_def is None or (
                    dataset_def.value is None and dataset_def.parameter_name not in data_path_param_names):
                remove_node_ids.append(str(node.id))
        return set(remove_node_ids)

    def _produce_module_runsettings(self, module: Component, module_node: GraphModuleNode):
        if module.runsettings is None:
            return None

        # do not remove this, or else module_node_run_setting does not make a difference
        module_node_run_setting = GraphModuleNodeRunSetting()
        module_node_run_setting.module_id = module._identifier
        module_node_run_setting.node_id = module_node.id
        module_node_run_setting.step_type = module._definition._module_dto.module_entity.step_type
        # Populate submission runsettings
        module_node_run_setting.run_settings, use_default_compute = _populate_submission_runsettings(module)
        module_node.use_graph_default_compute = use_default_compute
        return module_node_run_setting

    def _produce_edge_dataset_node_to_module_node(self, input_name, dataset_node, module_node):
        source = PortInfo(node_id=dataset_node.id, port_name=self.DATASOURCE_PORT_NAME)
        dest = PortInfo(node_id=module_node.id, port_name=input_name)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _produce_edge_module_node_to_module_node(self, input_name, output: Output, dest_module_node):
        # Note that we call topology sort before this so we could make sure the source module node has been added.
        source_module_node = self._get_node_by_component(output._owner)
        source = PortInfo(node_id=source_module_node.id, port_name=output.port_name)
        dest = PortInfo(node_id=dest_module_node.id, port_name=input_name)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _get_or_create_dataset_node(self, graph_entity: GraphDraftEntity, input: Input):
        # Need to be refined, what if a dataset provide different modes?
        input_hash = input._get_internal_data_source()
        if input_hash not in self._input_nodes:
            dataset_node = self._build_graph_datasource_node(input)
            graph_entity.dataset_nodes.append(dataset_node)
            self._nodes[dataset_node.id] = dataset_node
            self._input_nodes[input_hash] = dataset_node
        return self._input_nodes[input_hash]

    def _build_graph_module_node(self, module: Component, pipeline_regenerate_outputs: bool) -> GraphModuleNode:
        node_id = self._generate_node_id()
        regenerate_output = pipeline_regenerate_outputs \
            if pipeline_regenerate_outputs is not None else module.regenerate_output
        module_node = GraphModuleNode(id=node_id, module_id=module._identifier,
                                      regenerate_output=regenerate_output)
        module_node.module_parameters = []
        module_node.module_metadata_parameters = []
        self.module_node_to_graph_node_mapping[module._get_instance_id()] = node_id
        return module_node

    def _update_module_node_params(
        self, graph_entity: GraphDraftEntity, module_node: GraphModuleNode, module: Component,
    ):
        """Add module node parameters and update it with context.pipeline_parameters."""
        pipeline_parameters = self._context.pipeline_parameters
        node_parameters = module._get_default_parameters()
        node_pipeline_parameters = {}
        node_str_assignment_parameters = {}

        user_provided_params = module._build_params()

        def append_pipeline_parameter_to_interface(_pipeline_param_name):
            """
            Add necessary pipeline parameter to resolve parameter reference.

            If parameter is from pipeline parameters, add as node pipeline parameters
               to display the relationship.
            """
            exist = next((x for x in graph_entity.entity_interface.parameters
                          if x.name == _pipeline_param_name), None) is not None
            if not exist:
                value = pipeline_parameters[_pipeline_param_name]
                graph_entity.entity_interface.parameters.append(Parameter(
                    name=_pipeline_param_name, default_value=value,
                    is_optional=False, type=_python_type_to_type_code(type(value))))

        for param_name, param_value in user_provided_params.items():
            # TODO: Use an enum for value_type
            if isinstance(param_value, Input):
                param_value = param_value._get_internal_data_source()
            if isinstance(param_value, PipelineParameter):
                # Notice that param_value.name != param_name here
                if pipeline_parameters is not None and len(pipeline_parameters) > 0 and \
                        param_value.name in pipeline_parameters:
                    pipeline_param_name = param_value.name
                    node_pipeline_parameters[param_name] = pipeline_param_name
                    # Add necessary pipeline parameter to resolve parameter reference
                    append_pipeline_parameter_to_interface(pipeline_param_name)
                    if param_name in node_parameters:
                        del node_parameters[param_name]
                else:
                    # Some call from visualize may reach here,
                    # because they pass the pipeline parameter without default params.
                    node_parameters[param_name] = param_value.default_value
            elif isinstance(param_value, _ParameterAssignment):
                node_str_assignment_parameters[param_name] = param_value
                # Add necessary pipeline parameter to resolve parameter reference
                for name in param_value.expand_all_parameter_name_set():
                    # If name is sub pipeline parameter, it will not appear in pipeline parameter
                    if name in pipeline_parameters:
                        append_pipeline_parameter_to_interface(name)
                if param_name in node_parameters:
                    del node_parameters[param_name]
            else:
                node_parameters[param_name] = param_value

        # Put PipelineParameter as data_path_parameter for updating datapath list
        module_node.module_input_settings = []
        for input in module.inputs.values():
            input_setting = InputSetting(
                name=module._get_input_name_by_argument_name(input.name),
                data_store_mode=input.mode,
                path_on_compute=input._path_on_compute
            )
            module_node.module_input_settings.append(input_setting)

            input_data_source = input._get_internal_data_source()
            if not isinstance(input_data_source, PipelineParameter) or \
                    input_data_source.name in self._data_path_parameter_input:
                continue
            self._data_path_parameter_input[input_data_source.name] = input_data_source

        self._batch_append_module_node_parameter(module_node, node_parameters)
        self._batch_append_module_node_pipeline_parameters(module_node, node_pipeline_parameters)
        # Update formatter parts using new pipeline_parameters dict.
        self._batch_append_module_node_assignment_parameters(
            module_node, node_str_assignment_parameters, pipeline_parameters)

        module_node.module_output_settings = []
        # Resolve the pipeline datastore first
        pipeline_datastore = module._resolve_default_datastore()
        pipeline_datastore_name = pipeline_datastore.name if pipeline_datastore is not None else None

        for output in module.outputs.values():
            output_setting = OutputSetting(
                name=output.port_name,
                data_store_name=output.datastore.name if output.datastore else pipeline_datastore_name,
                data_store_mode=output.output_mode,
                path_on_compute=output._path_on_compute,
                data_reference_name=output.port_name,
                dataset_registration=output._dataset_registration,
                dataset_output_options=output._dataset_output_options,
            )
            module_node.module_output_settings.append(output_setting)

    def _update_data_path_parameter_list(self, graph_entity: GraphDraftEntity):
        """Update data path parameters with dataset parameters in context.pipeline_parameters."""
        def get_override_parameters_def(name, origin_val, pipeline_parameters):
            # Check if user choose to override with pipeline parameters
            if pipeline_parameters is not None and len(pipeline_parameters) > 0:
                for k, v in pipeline_parameters.items():
                    if k == name:
                        self._dataset_parameter_keys.add(k)
                        if isinstance(v, _GlobalDataset):
                            return _get_dataset_def_from_dataset(v)
                        elif isinstance(v, AbstractDataset):
                            v._ensure_saved(self._context.workspace)
                            return _get_dataset_def_from_dataset(v)
                        else:
                            raise UserErrorException('Invalid parameter value for dataset parameter: {0}'.format(k))

            return origin_val

        pipeline_parameters = self._context.pipeline_parameters
        for name, pipeline_parameter in self._data_path_parameter_input.items():
            dset = pipeline_parameter.default_value
            dataset_def = None

            if isinstance(dset, DatasetConsumptionConfig):
                dset = dset.dataset

            if isinstance(dset, AbstractDataset):
                dset._ensure_saved(self._context.workspace)
                dataset_def = _get_dataset_def_from_dataset(dset)

            if isinstance(dset, (_GlobalDataset, DataReference)):
                dataset_def = _get_dataset_def_from_dataset(dset)
            dataset_def = get_override_parameters_def(name, dataset_def, pipeline_parameters)
            if dataset_def is not None:
                exist = next((x for x in graph_entity.entity_interface.data_path_parameter_list
                              if x.name == name), None) is not None
                if not exist:
                    graph_entity.entity_interface.data_path_parameter_list.append(DataPathParameter(
                        name=name,
                        default_value=dataset_def.value,
                        is_optional=False,
                        data_type_id=DATAFRAMEDIRECTORY
                    ))

    LITERAL = _ParameterAssignment.LITERAL
    GRAPH_PARAMETER_NAME = _ParameterAssignment.PIPELINE_PARAMETER
    CONCATENATE = _ParameterAssignment.CONCATENATE

    def _batch_append_module_node_pipeline_parameters(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            param_assignment = ParameterAssignment(name=k, value=v, value_type=self.GRAPH_PARAMETER_NAME)
            module_node.module_parameters.append(param_assignment)

    def _batch_append_module_node_parameter(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            param_assignment = ParameterAssignment(name=k, value=v, value_type=self.LITERAL)
            module_node.module_parameters.append(param_assignment)

    def _batch_append_module_node_assignment_parameters(
            self, module_node: GraphModuleNode, params: dict, pipeline_parameters: dict):
        """
        Resolve _ParameterAssignment as multiple parameter assignment.

        :param module_node: the module node on graph.
        :type module_node: GraphModuleNode
        :param params: key is param name and value is _StrParameterAssignment.
        :type params: dict[str, _ParameterAssignment]
        :param pipeline_parameters: use pipeline_parameters from user input to update concatenate value.
        :type pipeline_parameters: dict[str, Any]
        """
        def get_assignments_to_concatenate(obj: _ParameterAssignment):
            assignments = []
            for part in obj.assignments:
                # part will be LITERAL/PIPELINE PARAMETER
                # part.str in pipeline parameters indicate it is root pipeline parameter
                if part.type == self.LITERAL or part.str in pipeline_parameters:
                    assignment = ParameterAssignment(value=part.str, value_type=part.type)
                else:
                    # If part is PipelineParameter but not in pipeline_parameters, then it is
                    # sub pipeline parameter, find value from values dict and resolve as LITERAL.
                    real_value = obj.assignments_values_dict[part.str].default_value
                    assignment = ParameterAssignment(value=real_value, value_type=self.LITERAL)
                assignments.append(assignment)
            return assignments

        for k, v in params.items():
            flattened_v = v.flatten()
            assignments_to_concatenate = get_assignments_to_concatenate(flattened_v)
            param_assignment = ParameterAssignment(
                name=k, value=flattened_v.get_value_with_pipeline_parameters(pipeline_parameters),
                value_type=self.CONCATENATE, assignments_to_concatenate=assignments_to_concatenate)
            module_node.module_parameters.append(param_assignment)

    def _append_module_meta_parameter(self, module_node: GraphModuleNode, param_name, param_value):
        param_assignment = ParameterAssignment(name=param_name, value=param_value, value_type=self.LITERAL)
        module_node.module_metadata_parameters.append(param_assignment)

    def _build_graph_datasource_node(self, input: Input) -> GraphDatasetNode:
        node_id = self._generate_node_id()
        input = input._get_internal_data_source()  # Get the actual input
        if isinstance(input, DatasetConsumptionConfig):
            input = input.dataset  # Get the AbstractDataset instance

        if isinstance(input, (AbstractDataset, _GlobalDataset, DataReference)):
            if isinstance(input, AbstractDataset):  # Make sure this dataset is saved.
                input._ensure_saved(self._context.workspace)

            dataset_def = _get_dataset_def_from_dataset(input)
            data_node = GraphDatasetNode(id=node_id, data_set_definition=dataset_def)
            return data_node

        if isinstance(input, PipelineParameter):
            dataset_def = DataSetDefinition(data_type_short_name=DATAFRAMEDIRECTORY,
                                            parameter_name=input.name)
            return GraphDatasetNode(id=node_id, data_set_definition=dataset_def)

        if isinstance(input, str) or isinstance(input, Path):
            dataset_def = DataSetDefinition(data_type_short_name=DATAFRAMEDIRECTORY,
                                            value=str(input))
            return GraphDatasetNode(id=node_id, data_set_definition=dataset_def)

        raise NotImplementedError("Unrecognized data source type: %r" % type(input))

    @staticmethod
    def _extract_mlc_compute_type(target_type):
        if target_type == AmlCompute._compute_type or target_type == RemoteCompute._compute_type or \
                target_type == HDInsightCompute._compute_type or target_type == ComputeInstance._compute_type:
            if target_type == AmlCompute._compute_type:
                return 'AmlCompute'
            elif target_type == ComputeInstance._compute_type:
                return 'ComputeInstance'
            elif target_type == HDInsightCompute._compute_type:
                return 'Hdi'
        return None

    def _generate_node_id(self) -> str:
        """
        Generate an 8-character node Id.

        :return: node_id
        :rtype: str
        """
        guid = str(uuid.uuid4())
        id_len = 8
        while guid[:id_len] in self._nodes:
            guid = str(uuid.uuid4())

        return guid[:id_len]


def _int_str_to_run_setting_ui_widget_type_enum(int_str_value):
    return list(RunSettingUIWidgetTypeEnum)[int(int_str_value)]


def _populate_submission_runsettings(component):
    runsettings_values = component._runsettings._get_flat_values()
    runsettings_definition = component._definition.runsettings
    # Union default values
    for p_id in runsettings_values:
        if runsettings_values[p_id] is None:
            runsettings_values[p_id] = runsettings_definition.params[p_id].default_value
    # Search space params
    search_space_params = _populate_sweep_search_space_runsettings(
        component, runsettings_definition, runsettings_values)
    runsettings = []
    runsettings.extend(search_space_params)
    compute_target_param = None
    use_root_pipeline_default_compute = True
    # RunSettings params
    for p in runsettings_definition.params.values():
        value = runsettings_values[p.id]
        if p.is_compute_target:
            # Correct:
            # If compute is inherit from top pipeline then use_root_pipeline_default_compute is True.
            # If compute is inherit from sub pipeline then use_root_pipeline_default_compute is False.
            compute_name, compute_type, use_root_pipeline_default_compute = component._compute
            if use_root_pipeline_default_compute:
                compute_name = None
                compute_type = None
            compute_target_param = RunSettingParameterAssignment(
                name=p.name, value=compute_name, value_type=0,
                use_graph_default_compute=use_root_pipeline_default_compute,
                mlc_compute_type=compute_type)
            runsettings.append(compute_target_param)
        else:
            value = runsettings_values[p.id]
            should_json_dumps = (value is not None and
                                 p.parameter_type == RunSettingParameterType.json_string and
                                 not isinstance(value, str))
            if should_json_dumps:
                value = json.dumps(value)
            runsettings.append(RunSettingParameterAssignment(
                name=p.name, value=value, value_type=0))
    # Compute runsettings
    # Always add compute settings
    # Since module may use default compute, we don't have to detect this, MT will handle
    if compute_target_param is not None and len(runsettings_definition.compute_params) > 0:
        compute_runsettings_values = component._k8srunsettings._get_flat_values()
        compute_settings = []
        for p in runsettings_definition.compute_params.values():
            compute_settings.append(
                RunSettingParameterAssignment(name=p.name,
                                              value=compute_runsettings_values[p.id],
                                              value_type=0))

        compute_target_param.compute_run_settings = compute_settings
    return runsettings, use_root_pipeline_default_compute


def _populate_sweep_search_space_runsettings(component, runsettings_definition, runsettings_values):
    algorithm = next(
        (p for p in runsettings_definition.params.values() if p.linked_parameters is not None), None)
    search_space_params = []
    if algorithm is not None:
        algorithm_value = runsettings_values[algorithm.id]
        # Get linked parameters
        linked_params = algorithm.linked_parameters.keys()
        # Get default values
        default_values = {p: {} for p in linked_params}
        if algorithm_value == algorithm.default_value:
            # Only get default values when algorithm is default value
            for p in runsettings_definition.search_space_params.values():
                if p.linked_parameters is None:
                    continue
                for k, v in p.linked_parameters.items():
                    default_values[k][p.argument_name] = v
        # Get user inputs
        input_values = {k: v for k, v in component._parameter_params.items() if k in linked_params}
        # Merge default values and user inputs
        for p in linked_params:
            if input_values[p] is None:
                input_values[p] = {}
            input_values[p] = {**(default_values[p]), **(input_values[p])}

        # process type
        type_spec = next(
            (p.enabled_by[algorithm.name][algorithm_value]
             for p in runsettings_definition.search_space_params.values() if p.argument_name == 'type' and
             algorithm.name in p.enabled_by and algorithm_value in p.enabled_by[algorithm.name]), None)
        if type_spec is not None:
            # Get params enabled by type for each linked parameter
            for linked_p_name in linked_params:
                linked_p_value = input_values.get(linked_p_name)
                if linked_p_value is None:
                    # TODO: rasie exception here?
                    continue
                type_value = linked_p_value.get(type_spec.argument_name)
                if type_value is None:
                    # TODO: rasie exception here?
                    continue
                # Try to validate the type value, if not valid, ignore it
                # TODO: put it in component.validation? and throw exception when invalid?
                if type_value not in type_spec.enum:
                    continue
                # Add type value to submission runsettings
                search_space_params.append(RunSettingParameterAssignment(
                    name=type_spec.name,
                    value=type_value,
                    value_type=0,
                    linked_parameter_name=linked_p_name
                ))
                # params enabled by type
                params_by_type = [
                    p for p in runsettings_definition.search_space_params.values()
                    if type_spec.name in p.enabled_by and type_value in p.enabled_by[type_spec.name]]
                for p in params_by_type:
                    search_space_params.append(RunSettingParameterAssignment(
                        name=p.name,
                        value=linked_p_value.get(p.argument_name),
                        value_type=0,
                        linked_parameter_name=linked_p_name
                    ))
    return search_space_params
