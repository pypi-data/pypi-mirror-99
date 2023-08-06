# Python SCALE Codec Library
#
# Copyright 2018-2020 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json


def load_type_registry_preset(name):
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(name))
    return load_type_registry_file(path)


def load_type_registry_file(file_path):

    with open(os.path.abspath(file_path), 'r') as fp:
        data = fp.read()

    return json.loads(data)
