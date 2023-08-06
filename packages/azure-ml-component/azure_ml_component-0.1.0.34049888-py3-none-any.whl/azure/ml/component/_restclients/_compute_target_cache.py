# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import time


class _ComputeTargetCacheItem:
    """ComputeTargetCacheItem.
    :param value: The instance of ExperimentComputeMetaInfo
    :type value: ExperimentComputeMetaInfo
    """

    expired_time_in_seconds = 60

    def __init__(self, value):
        self.value = value
        self.cache_time = time.time()

    def is_expired(self):
        return time.time() - self.cache_time > self.expired_time_in_seconds


class _ComputeTargetCache:
    """Compute target cache."""

    def __init__(self):
        self._cache_dict = {}

    def set_item(self, compute_name, item: _ComputeTargetCacheItem):
        self._cache_dict[compute_name] = item

    def get_item(self, compute_name):
        return self._cache_dict.get(compute_name, None)
