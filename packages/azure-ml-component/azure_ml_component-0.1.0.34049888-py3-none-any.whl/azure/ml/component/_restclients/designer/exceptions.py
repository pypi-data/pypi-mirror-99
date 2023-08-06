# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import types
from functools import wraps
from typing import List

from azureml._restclient.exceptions import ServiceException
from .models import ErrorResponseException


def _is_user_error(http_status_code):
    return 400 <= http_status_code < 500


class ServiceError(Exception):
    """General error when interacting with the http server."""

    def __init__(self, message):
        super().__init__(message)


class ComponentServiceError(ServiceException):
    """General error when interacting with the component service."""

    def __init__(self, error_response_exception):
        super().__init__(error_response_exception)

    @classmethod
    def from_response_exception(cls, e: ErrorResponseException):
        from azure.ml.component._api._utils import get_value_by_key_path
        res = e.response

        json = res.json()
        error_code = get_value_by_key_path(json, 'error/innerError/innerError/code', None)

        # This is for catching conflict error.
        if error_code == 'ComponentVersionConflict':
            return ComponentAlreadyExistsError(e)
        else:
            return ComponentServiceError(e)


class ComponentAlreadyExistsError(ComponentServiceError):
    pass


class AggregatedComponentError(ServiceError):
    """Aggregated component error."""

    def __init__(self, exceptions: List):
        super().__init__(str(exceptions))


def error_wrapper(exception: ErrorResponseException):
    """Try to wrap ErrorResponseException to ComponentServiceError, return original exception if failed."""
    try:
        return ComponentServiceError.from_response_exception(exception)
    except BaseException:
        return exception


def try_to_find_request_id_from_params(args, kwargs):
    """Try to find request id from positional arguments and key value arguments

    Note: This function only try to find request id from auto-generated service call methods.
    eg: ComponentOperations.get_component( ..., custom_headers=None, ...)
    :param args: positional arguments
    :param kwargs: key value arguments
    :return: Request id or None if request id not found
    """
    request_id_key = 'x-ms-client-request-id'
    # find in positional args
    for arg in args:
        if isinstance(arg, dict):
            if request_id_key in arg.keys():
                return arg.get(request_id_key)
    # find in kwargs, we assume request id can only be found in value of "custom_headers"
    if 'custom_headers' in kwargs.keys():
        return kwargs['custom_headers'].get(request_id_key, None)
    return None


def wrap_api_call_exception():
    """When calling rest apis, Wrap ErrorResponseException to ComponentServiceError. For other exceptions, add
    request id to it.
    """

    def wrap_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ErrorResponseException as e:
                raise error_wrapper(e)
            except BaseException as e:
                error_msg = "Got error {0}: '{1}' while calling {2}".format(e.__class__.__name__, e, f.__name__)
                # add request id if possible
                request_id = try_to_find_request_id_from_params(args, kwargs)
                if request_id:
                    error_msg = '{} (RequestId: {})'.format(error_msg, request_id)
                raise ServiceError(error_msg) from e

        return wrapper

    return wrap_decorator


def wrap_api_caller_methods_with_error_handling(obj, error_handler=wrap_api_call_exception):
    """Wrap all methods of api caller with error handling.
    All API calls in rest client are defined as method, so we only wrap methods.
    Note, class methods will be wrapped, static methods won't.

    For example
    Class Deserializer:
        def __call__():
            pass
    Class ComponentOperations:
        def __init__(self):
            self._deserialize = Deserializer
        def method1():
    When wrapping a ComponentOperations object, only method1 will be wrapped with error handling.

    :param obj: The object being wrapped.
    :param error_handler: The decorator used to wrap methods.
    """
    for attribute_name in dir(obj):
        if not attribute_name.startswith('__'):
            attr = getattr(obj, attribute_name)
            if isinstance(attr, types.MethodType):
                setattr(obj, attribute_name, error_handler()(attr))
