# Copyright (C) 2021 Johan Fleury <jfleury@arcaik.net>
#
# This file is part of targetd-client.
#
# targetd-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# targetd-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with targetd-client.  If not, see <https://www.gnu.org/licenses/>.

"""
This is a simple type hint definition for humanize.naturalsize that can be
removed once jmoiron/humanize#150 [1] is merged and released

[1]: https://github.com/jmoiron/humanize/pull/150/files
"""

from typing import Union

def naturalsize(
    value: Union[int, float, str],
    binary: bool = False,
    gnu: bool = False,
    format: str = "%.1f",
) -> str: ...
