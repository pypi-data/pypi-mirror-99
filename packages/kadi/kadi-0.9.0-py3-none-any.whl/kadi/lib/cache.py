# Copyright 2020 Karlsruhe Institute of Technology
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
from functools import wraps
from inspect import signature

from flask import current_app
from flask import g
from flask import has_request_context


def _make_hashable(obj):
    if isinstance(obj, (list, set)):
        return tuple(_make_hashable(item) for item in obj)

    if isinstance(obj, dict):
        return frozenset((k, _make_hashable(v)) for k, v in obj.items())

    return obj


# The following function is a slightly modified version of indico's memoize_request
# function, which is available at the following URL:
# https://github.com/indico/indico/blob/v2.3.3/indico/util/caching.py
#
# indico is licensed under the MIT license:
#
# MIT License
#
# Copyright (c) European Organization for Nuclear Research (CERN)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def memoize_request(func):
    """Decorator to cache a function call's result during a request.

    Uses an in-memory dictionary as cache that will be deleted again after the current
    request. The functions fully qualified name and arguments will be used as key to
    store its result for following calls.

    Disabled during testing.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not has_request_context() or current_app.testing:
            return func(*args, **kwargs)

        try:
            cache = g.memoize_cache
        except AttributeError:
            g.memoize_cache = cache = {}

        bound_args = signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        key = (
            func.__module__,
            func.__name__,
            _make_hashable(dict(bound_args.arguments)),
        )

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return decorated_function
