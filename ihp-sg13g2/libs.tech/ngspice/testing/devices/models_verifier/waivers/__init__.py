# =========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

"""
Milestone M2 -- waiver / baseline system.

`waiver.py`   : load + evaluate per-device YAML waiver files (`waivers/<device>.yaml`).
`generate.py` : snapshot a device's CURRENT (non-waived) failures into that YAML file
                (`python -m models_verifier.waivers.generate --device <d>`).
"""
