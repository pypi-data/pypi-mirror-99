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
from marshmallow.validate import Length

from .models import Tag
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import NonEmptyString


class TagSchema(KadiSchema):
    """Schema to represent tags.

    See :class:`.Tag`.
    """

    name = NonEmptyString(
        required=True,
        filters=[lower, normalize],
        validate=Length(max=Tag.Meta.check_constraints["name"]["length"]["max"]),
    )
