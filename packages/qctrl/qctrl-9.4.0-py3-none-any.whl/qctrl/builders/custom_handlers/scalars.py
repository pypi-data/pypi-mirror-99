# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
# pylint:disable=missing-module-docstring,too-many-ancestors
import json
from datetime import datetime
from typing import Any

import pythonflow as pf
import pytz
from dateutil.parser import parse
from qctrlcommons.serializers import (
    DataTypeDecoder,
    DataTypeEncoder,
)

from qctrl.builders.graphql_utils.handlers.base import BaseHandler
from qctrl.builders.graphql_utils.handlers.mixins import ScalarMixin


def _encode_custom_scalar(value: Any) -> Any:
    """Encodes a custom scalar value."""
    result = json.dumps(value, cls=DataTypeEncoder)
    return json.dumps(result)


def _decode_custom_scalar(value: Any) -> Any:
    """Decodes a custom scalar value."""
    return json.loads(value, cls=DataTypeDecoder)


def _decode_datetime_scalar(value: str) -> datetime:
    """
    Decode a datetime scalar value.
    """
    return parse(value)


def _decode_unix_scalar(value: str) -> datetime:
    """
    Decode a unixtime scalar value.
    """
    return datetime.fromtimestamp(int(value)).astimezone(pytz.utc)


class JsonStringScalarHandler(ScalarMixin, BaseHandler):
    """Custom scalar handler for JsonString."""

    _scalar_name = "JsonString"
    _scalar_encoder = _encode_custom_scalar
    _scalar_decoder = _decode_custom_scalar
    _scalar_allowed_type = str
    scalar_type_hint = str


class DateTimeScalarHandler(ScalarMixin, BaseHandler):
    """Custom scalar handler for DateTime."""

    _scalar_name = "DateTime"
    _scalar_allowed_type = datetime
    _scalar_decoder = _decode_datetime_scalar
    scalar_type_hint = datetime


class GraphScalarHandler(ScalarMixin, BaseHandler):
    """Custom scalar handler for Graph."""

    _scalar_name = "Graph"
    _scalar_encoder = _encode_custom_scalar
    _scalar_decoder = _decode_custom_scalar
    _scalar_allowed_type = pf.core.Graph
    scalar_type_hint = pf.core.Graph


class JsonDictScalarHandler(ScalarMixin, BaseHandler):
    """Custom scalar handler for JsonDict."""

    _scalar_name = "JsonDict"
    _scalar_encoder = _encode_custom_scalar
    _scalar_decoder = _decode_custom_scalar
    _scalar_allowed_type = dict
    scalar_type_hint = dict


class UnixTimeScalarHandler(ScalarMixin, BaseHandler):
    """Custom scalar handler for UnixTime."""

    _scalar_name = "UnixTime"
    _scalar_allowed_type = datetime
    _scalar_decoder = _decode_unix_scalar
    scalar_type_hint = datetime
