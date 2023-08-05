# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from typing_extensions import TypedDict

import qumulo.lib.request as request

from qumulo.lib.auth import Credentials
from qumulo.lib.request import RestResponse


class ApiVersionInfo(TypedDict):
    revision_id: str
    build_id: str
    flavor: str
    build_date: str


@request.request
def version(
    conninfo: request.Connection, credentials: Credentials
) -> request.RestResponse:
    method = 'GET'
    uri = '/v1/version'
    return request.rest_request(conninfo, credentials, method, uri)


@request.request
def numeric_version(
    conninfo: request.Connection, credentials: Credentials
) -> request.RestResponse:
    # e.g., {... revision_id: Qumulo Core 1.2.3, ...} -> "1.2.3"
    numeric = version(conninfo, credentials)[0]['revision_id'].rpartition(' ')[2]
    return RestResponse(numeric, None)
