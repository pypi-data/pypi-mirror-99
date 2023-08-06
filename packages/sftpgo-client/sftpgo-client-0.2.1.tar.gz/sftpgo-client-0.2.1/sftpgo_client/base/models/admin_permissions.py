from enum import Enum


class AdminPermissions(str, Enum):
    VALUE_0 = "*"
    ADD_USERS = "add_users"
    EDIT_USERS = "edit_users"
    DEL_USERS = "del_users"
    VIEW_USERS = "view_users"
    VIEW_CONNS = "view_conns"
    CLOSE_CONNS = "close_conns"
    VIEW_STATUS = "view_status"
    MANAGE_ADMINS = "manage_admins"
    QUOTA_SCANS = "quota_scans"
    MANAGE_SYSTEM = "manage_system"
    MANAGE_DEFENDER = "manage_defender"
    VIEW_DEFENDER = "view_defender"

    def __str__(self) -> str:
        return str(self.value)
