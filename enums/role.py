from enum import StrEnum


class UserRoleEnum(StrEnum):
    ADMIN = "admin"
    HOSTESS = "hostess"
    COOK = "cook"
    DELIVERY = "delivery"
    WAITER = "waiter"
