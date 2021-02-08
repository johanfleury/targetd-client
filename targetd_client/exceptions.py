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

class TargetdException(Exception):
    # Common
    INVALID = -1
    NAME_CONFLICT = -50
    NO_SUPPORT = -153
    UNEXPECTED_EXIT_CODE = -303
    INVALID_ARGUMENT = -32602

    # Specific to block
    EXISTS_INITIATOR = -52
    NOT_FOUND_VOLUME = -103
    NOT_FOUND_VOLUME_EXPORT = -151
    NOT_FOUND_VOLUME_GROUP = -152
    NOT_FOUND_ACCESS_GROUP = -200
    VOLUME_MASKED = -303
    NO_FREE_HOST_LUN_ID = -1000

    # Specific to FS/NFS
    EXISTS_CLONE_NAME = -51
    EXISTS_FS_NAME = -53
    NOT_FOUND_FS = -104
    INVALID_POOL = -110
    NOT_FOUND_SS = -112
    NOT_FOUND_NFS_EXPORT = -400
    NFS_NO_SUPPORT = -401

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
