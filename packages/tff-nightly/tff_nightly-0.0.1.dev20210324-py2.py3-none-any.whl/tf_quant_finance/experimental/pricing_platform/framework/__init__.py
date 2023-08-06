# Lint as: python3
# Copyright 2020 Google LLC
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
"""Framework module."""

from tf_quant_finance.experimental.pricing_platform.framework import core
from tf_quant_finance.experimental.pricing_platform.framework import equity_instruments
from tf_quant_finance.experimental.pricing_platform.framework import market_data
from tf_quant_finance.experimental.pricing_platform.framework import rate_instruments


from tensorflow.python.util.all_util import remove_undocumented  # pylint: disable=g-direct-tensorflow-import

_allowed_symbols = [
    "core",
    "equity_instruments",
    "market_data",
    "rate_instruments",
]

remove_undocumented(__name__, _allowed_symbols)
