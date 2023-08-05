# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

"""
Author: Boris Feld

This module contains comet generated Exceptions

"""

from ._typing import Any, Dict, Optional
from .logging_messages import (
    INVALID_API_KEY,
    INVALID_PROJECT_NAME,
    INVALID_REST_API_KEY,
    INVALID_WORKSPACE_NAME,
)
from .utils import format_version_number


class CometException(Exception):
    """ Base-class for all comet specific exceptions
    """


class NotParametrizedException(CometException):
    def __str__(self):
        return "Please call set_params or set_params_file before calling get_suggestion"


class ValidationError(CometException):
    pass


class AuthenticationError(CometException):
    pass


class NoMoreSuggestionsAvailable(CometException):
    def __str__(self):
        return "No more suggestions available!"


class InvalidAPIKey(CometException):

    log_message = INVALID_API_KEY

    def __init__(self, api_key):
        super(CometException, self).__init__()
        self.api_key = api_key
        self.args = (self.api_key,)


class InvalidRestAPIKey(CometException):

    log_message = INVALID_REST_API_KEY

    def __init__(self, rest_api_key):
        super(CometException, self).__init__()
        self.rest_api_key = rest_api_key
        self.args = (self.rest_api_key,)


class InvalidWorkspace(CometException):

    log_message = INVALID_WORKSPACE_NAME

    def __init__(self, workspace):
        super(CometException, self).__init__()
        self.workspace = workspace
        self.args = (self.workspace,)


class ProjectNameEmpty(CometException):

    log_message = INVALID_PROJECT_NAME

    def __init__(self):
        super(CometException, self).__init__()
        self.args = tuple()


class InvalidOfflineDirectory(CometException):
    def __init__(self, directory, reason):
        self.directory = directory
        self.reason = reason

    def __str__(self):
        msg = "Invalid offline directory: %s\nReason:%s"
        return msg % (self.directory, self.reason)


class InterruptedExperiment(KeyboardInterrupt):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        msg = "The experiment has been stopped by user %s from Comet"
        return msg % self.username


class RPCFunctionAlreadyRegistered(CometException):
    def __init__(self, function_name):
        self.function_name = function_name

    def __str__(self):
        msg = "The callback name %r is already taken"
        return msg % self.function_name


class LambdaUnsupported(CometException):
    def __init__(self):
        pass

    def __str__(self):
        return "Lambda are not supported as remote actions"


class BadCallbackArguments(CometException):

    msg = "Remote action %r should accepts at least one argument named `experiment`"

    def __init__(self, callback):
        self.callback = callback

    def __str__(self):
        return self.msg % self.callback


class ExperimentAlreadyUploaded(CometException):
    msg = "Experiment with id %r was already uploaded"

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

    def __str__(self):
        return self.msg % self.experiment_id


class FileIsTooBig(CometException):
    msg = "File %r size %d is greater than the upload limit %d"

    def __init__(self, file_path, file_size, max_size):
        self.file_path = file_path
        self.file_size = file_size
        self.max_size = max_size

    def __str__(self):
        return self.msg % (self.file_path, self.file_size, self.max_size)


class OptimizerException(CometException):
    pass


class InvalidOptimizerParameters(CometException):
    pass


class CometRestApiException(CometException):
    def __init__(self, method, response):
        super(CometRestApiException, self).__init__()
        self.method = method
        self.response = response
        try:
            self.safe_json_response = (
                self.response.json()
            )  # type: Optional[Dict[Any, Any]]
        except ValueError:
            self.safe_json_response = None

    def __str__(self):
        try:
            msg = self.response.json().get("msg", None)
        except ValueError:
            msg = None

        if msg:
            return "%s %s failed with status code %s: %s" % (
                self.method,
                self.response.url,
                self.response.status_code,
                msg,
            )
        else:
            return "%s %s failed with status code %s" % (
                self.method,
                self.response.url,
                self.response.status_code,
            )


class CometRestApiValueError(CometRestApiException):
    def __init__(self, method, message, response):
        super(CometRestApiValueError, self).__init__(method, response)
        self.message = message

    def __str__(self):
        return "%s %s %s; failed with status code %s" % (
            self.method,
            self.response.url,
            self.message,
            self.response.status_code,
        )


class PaymentRequired(CometRestApiException):
    def __str__(self):
        try:
            return self.response.json().get("msg", "")
        except ValueError:
            return None


class NotFound(CometRestApiException):
    def __str__(self):
        try:
            return self.response.json().get("msg", "")
        except ValueError:
            return None


class QueryException(CometException):
    pass


class BackendVersionTooOld(CometException):
    msg = """The API client requires backend version {minimal_backend_version} or higher.
Detected an incompatible backend version {backend_version} (at {backend_url}).
Please update your backend version or inform your administrator to update it.
In the mean-time, you can downgrade the python SDK to a version compatible with your backend with: `pip install -U 'comet-ml<3'`"""

    def __init__(self, backend_url, backend_version, minimal_backend_version):
        self.backend_url = backend_url
        self.backend_version = backend_version
        self.minimal_backend_version = minimal_backend_version

    def __str__(self):
        return self.msg.format(
            backend_url=self.backend_url,
            backend_version=format_version_number(self.backend_version),
            minimal_backend_version=format_version_number(self.minimal_backend_version),
        )


"""
SDK Error Code mapping, names comes from the backend
"""

API_KEY_NOT_REGISTERED = 90212
EXPERIMENT_ALREADY_EXISTS = 90999
INVALID_OPTIMIZATION_ID = 5124123
NO_PROJECT_NAME_SPECIFIED = 98219
NON_EXISTING_TEAM = 90219
