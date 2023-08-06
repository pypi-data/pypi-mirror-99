# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from enum import Enum
from pathlib import Path
from azureml.core import Dataset
from azureml.data.data_reference import DataReference
from azureml.data.datapath import DataPath
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

from ._dataset import _GlobalDataset


class PipelineParameter(object):
    """Defines a parameter in a pipeline execution.

    Use PipelineParameters to construct versatile Pipelines which can be resubmitted later with varying
    parameter values. Note that we do not expose this as part of our public API yet. This is only intended for
    internal usage.

    :param name: The name of the pipeline parameter.
    :type name: str
    :param default_value: The default value of the pipeline parameter.
    :type default_value: literal values
    :param _auto_wrap_for_build: Indicate whether the pipeline parameter is wrapped for build definition.
    :type _auto_wrap_for_build: bool
    """
    def __init__(self, name, default_value, _auto_wrap_for_build=False):
        default_value = default_value.value if isinstance(default_value, Enum) else default_value

        self.name = name
        self.default_value = default_value
        self._auto_wrap_for_build = _auto_wrap_for_build

        if not isinstance(default_value, int) and not isinstance(default_value, str) and \
            not isinstance(default_value, bool) and not isinstance(default_value, float) \
                and not isinstance(default_value, Path) \
                and not isinstance(default_value, DataPath) and not isinstance(default_value, Dataset) \
                and not isinstance(default_value, DatasetConsumptionConfig) \
                and not isinstance(default_value, AbstractDataset) and not isinstance(default_value, _GlobalDataset) \
                and not isinstance(default_value, DataReference) \
                and default_value is not None:
            raise ValueError('Default value is of unsupported type: {0}'.format(type(default_value).__name__))

    def __repr__(self):
        """
        __repr__ override.

        :return: The representation of the PipelineParameter.
        :rtype: str
        """
        return "PipelineParameter(name={0}, default_value={1})".format(self.name, self.default_value)

    def __str__(self):
        """
        __str__ override.

        :return: The placeholder of the PipelineParameter.
        :rtype: str
        """
        return "@@{}@@".format(self.name)

    def _serialize_to_dict(self):
        if isinstance(self.default_value, DataPath):
            return {"type": "datapath",
                    "default": self.default_value._serialize_to_dict()}
        else:
            param_type = "string"
            if isinstance(self.default_value, int):
                param_type = "int"
            if isinstance(self.default_value, float):
                param_type = "float"
            if isinstance(self.default_value, bool):
                param_type = "bool"
            return {"type": param_type,
                    "default": self.default_value}
