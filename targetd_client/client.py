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

import requests
import uuid

from typing import List, Dict, Any, Optional

from .exceptions import TargetdException


class TargetdClient(object):
    def __init__(
        self, url: str, user: str, password: str, insecure_skip_verify: bool = False
    ):
        self.url = url
        self.user = user
        self.password = password
        self.insecure_skip_verify = insecure_skip_verify

    def request(self, method: str, params: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        request_id = int(uuid.uuid4())

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        r = requests.post(
            f"{self.url}/targetrpc",
            auth=(self.user, self.password),
            json=payload,
            verify=not self.insecure_skip_verify,
        )
        r.raise_for_status()

        response = r.json()

        if response["id"] != request_id:
            raise TargetdException(
                -1, f"expected request id {request_id}, got {response['id']}"
            )

        error = response.get("error", None)
        if error:
            raise TargetdException(error["code"], error["message"])

        result: List[Dict[str, Any]] = response["result"]
        return result

    def get_first_available_lun(self) -> int:
        existing_luns = set(export["lun"] for export in self.export_list())

        i = 0
        while True:
            if i not in existing_luns:
                break
            i += 1

        return i

    def pool_list(self) -> List[Dict[str, Any]]:
        return self.request("pool_list")

    def vol_list(self, pool: str) -> List[Dict[str, Any]]:
        return self.request("vol_list", {"pool": pool})

    def vol_create(self, pool: str, name: str, size: int) -> None:
        self.request("vol_create", {"pool": pool, "name": name, "size": size})

    def vol_destroy(self, pool: str, name: str) -> None:
        self.request("vol_destroy", {"pool": pool, "name": name})

    def vol_copy(self, pool: str, vol_orig: str, vol_new: str, size: int) -> None:
        self.request(
            "vol_copy",
            {"pool": pool, "vol_orig": vol_orig, "vol_new": vol_new, "size": size},
        )

    def export_list(self) -> List[Dict[str, Any]]:
        return self.request("export_list")

    def export_create(
        self, pool: str, vol: str, initiator_wwn: str, lun: Optional[int] = None
    ) -> int:
        existing_export = next(
            filter(
                lambda x: x["pool"] == pool
                and x["vol_name"] == vol
                and x["initiator_wwn"] == initiator_wwn,
                self.export_list(),
            ),
            None,
        )

        if existing_export and lun is None:
            return int(existing_export["lun"])

        if lun is None:
            lun = self.get_first_available_lun()

        self.request(
            "export_create",
            {
                "pool": pool,
                "vol": vol,
                "initiator_wwn": initiator_wwn,
                "lun": lun,
            },
        )

        return lun

    def export_destroy(self, pool: str, vol: str, initiator_wwn: str) -> None:
        self.request(
            "export_destroy", {"pool": pool, "vol": vol, "initiator_wwn": initiator_wwn}
        )

    def initiator_set_auth(
        self,
        initiator_wwn: str,
        in_user: str,
        in_pass: str,
        out_user: str,
        out_pass: str,
    ) -> None:
        self.request(
            "initiator_set_auth",
            {
                "initiator_wwn": initiator_wwn,
                "in_user": in_user,
                "in_pass": in_pass,
                "out_user": out_user,
                "out_pass": out_pass,
            },
        )

    def initiator_list(self, standalone_only: bool = False) -> List[Dict[str, Any]]:
        return self.request("initiator_list", {"standalone_only": standalone_only})

    def access_group_list(self) -> List[Dict[str, Any]]:
        return self.request("access_group_list")

    def access_group_create(
        self, ag_name: str, init_id: str, init_type: str = "iscsi"
    ) -> None:
        self.request(
            "access_group_create",
            {"ag_name": ag_name, "init_id": init_id, "init_type": init_type},
        )

    def access_group_destroy(self, ag_name: str) -> None:
        self.request("access_group_destroy", {"ag_name": ag_name})

    def access_group_init_add(
        self, ag_name: str, init_id: str, init_type: str = "iscsi"
    ) -> None:
        self.request(
            "access_group_init_add",
            {"ag_name": ag_name, "init_id": init_id, "init_type": init_type},
        )

    def access_group_init_del(
        self, ag_name: str, init_id: str, init_type: str = "iscsi"
    ) -> None:
        self.request(
            "access_group_init_del",
            {"ag_name": ag_name, "init_id": init_id, "init_type": init_type},
        )

    def access_group_map_list(self) -> List[Dict[str, Any]]:
        return self.request(
            "access_group_map_list",
        )

    def access_group_map_create(
        self,
        pool_name: str,
        vol_name: str,
        ag_name: str,
        h_lun_id: Optional[int] = None,
    ) -> None:
        self.request(
            "access_group_map_create",
            {
                "pool_name": pool_name,
                "vol_name": vol_name,
                "ag_name": ag_name,
                "h_lun_id": h_lun_id,
            },
        )

    def access_group_map_destroy(
        self, pool_name: str, vol_name: str, ag_name: str
    ) -> None:
        self.request(
            "access_group_map_destroy",
            {"pool_name": pool_name, "vol_name": vol_name, "ag_name": ag_name},
        )

    def fs_list(self) -> List[Dict[str, Any]]:
        return self.request(
            "fs_list",
        )

    def fs_destroy(self, uuid: str) -> None:
        self.request("fs_destroy", {"uuid": uuid})

    def fs_create(self, pool_name: str, name: str, size_bytes: int) -> None:
        self.request(
            "fs_create",
            {"pool_name": pool_name, "name": name, "size_bytes": size_bytes},
        )

    def fs_clone(self, fs_uuid: str, dest_fs_name: str, snapshot_id: str) -> None:
        self.request(
            "fs_clone",
            {
                "fs_uuid": fs_uuid,
                "dest_fs_name": dest_fs_name,
                "snapshot_id": snapshot_id,
            },
        )

    def ss_list(self, fs_uuid: str) -> List[Dict[str, Any]]:
        return self.request("ss_list", {"fs_uuid": fs_uuid})

    def fs_snapshot(self, fs_uuid: str, dest_ss_name: str) -> None:
        self.request("fs_snapshot", {"fs_uuid": fs_uuid, "dest_ss_name": dest_ss_name})

    def fs_snapshot_delete(self, fs_uuid: str, ss_uuid: str) -> None:
        self.request("fs_snapshot_delete", {"fs_uuid": fs_uuid, "ss_uuid": ss_uuid})

    def nfs_export_auth_list(self) -> List[Dict[str, Any]]:
        return self.request("nfs_export_auth_list")

    def nfs_export_list(self) -> List[Dict[str, Any]]:
        return self.request("nfs_export_list")

    def nfs_export_add(
        self, host: str, path: str, options: List[str], chown: str
    ) -> None:
        self.request(
            "nfs_export_add",
            {"host": host, "path": path, "options": options, "chown": chown},
        )

    def nfs_export_remove(self, host: str, path: str) -> None:
        self.request("nfs_export_remove", {"host": host, "path": path})
