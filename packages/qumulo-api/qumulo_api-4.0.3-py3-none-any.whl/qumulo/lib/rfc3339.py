# Copyright (c) 2020 Qumulo, Inc.
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

# XXX: Please add types to the functions in this file. Static type checking in
# Python prevents bugs!
# mypy: ignore-errors


import datetime
import re


def parse_rfc3339_time(time_string):
    """
    Convert an rfc3339 time to a datetime object. This is the standard JSON
    encoding for struct time in the C code (see core/time/rfc_3339.c).
    """
    return datetime.datetime.strptime(
        re.sub(r'[.].*Z$', 'Z', time_string), '%Y-%m-%dT%H:%M:%SZ'
    )
