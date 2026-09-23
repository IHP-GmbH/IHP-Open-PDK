########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

import os
import sys


python_directory = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "python"))
sys.path.insert(0, python_directory)

api_directory = os.path.join(python_directory, "pycell4klayout-api", "source", "python")
sys.path.insert(0, api_directory)

from sg13g2_pycell_lib.ihp.utility_functions import sprintf


assert sprintf("value=%s", "test") == "value=test"
assert sprintf("%s=%d", "count", 3) == "count=3"
assert sprintf("literal") == "literal"

print("sprintf regression test passed")
