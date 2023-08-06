# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from fastestimator import architecture, backend, dataset, layers, op, schedule, summary, trace, util, xai
from fastestimator.estimator import Estimator, enable_deterministic
from fastestimator.network import Network, build
from fastestimator.pipeline import Pipeline

# Fix known bugs with libraries which use multi-processing in a way which conflicts with pytorch data loader
import cv2
cv2.setNumThreads(0)
try:
    import SimpleITK as sitk
    sitk.ProcessObject.SetGlobalDefaultNumberOfThreads(1)
except ModuleNotFoundError:
    pass

__version__ = '1.1.3'
fe_deterministic_seed = None
