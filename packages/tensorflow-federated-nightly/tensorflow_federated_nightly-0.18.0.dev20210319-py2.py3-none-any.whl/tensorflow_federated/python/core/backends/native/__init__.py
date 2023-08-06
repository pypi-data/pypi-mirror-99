# Copyright 2020, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Libraries for interacting with native backends."""

from tensorflow_federated.python.core.backends.native.compiler import transform_mathematical_functions_to_tensorflow
from tensorflow_federated.python.core.backends.native.compiler import transform_to_native_form
from tensorflow_federated.python.core.backends.native.execution_contexts import create_local_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import create_remote_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import create_sizing_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import create_thread_debugging_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import set_local_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import set_remote_execution_context
from tensorflow_federated.python.core.backends.native.execution_contexts import set_thread_debugging_execution_context
