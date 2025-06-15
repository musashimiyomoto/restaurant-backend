from enums.order import OrderStatusEnum
from enums.role import UserRoleEnum

ROLE_STATUS_PERMISSIONS = {
    UserRoleEnum.HOSTESS: {
        OrderStatusEnum.CLIENT_OPENED: [
            OrderStatusEnum.PENDING_CONFIRMATION,
        ],
        OrderStatusEnum.PENDING_CONFIRMATION: [
            OrderStatusEnum.CONFIRMED,
            OrderStatusEnum.CANCELLED,
        ],
    },
    UserRoleEnum.COOK: {
        OrderStatusEnum.CONFIRMED: [
            OrderStatusEnum.COOKING,
        ],
        OrderStatusEnum.COOKING: [
            OrderStatusEnum.WAITING_COURIER,
            OrderStatusEnum.WAITING_SERVER,
            OrderStatusEnum.WAITING_PICKUP,
        ],
    },
    UserRoleEnum.DELIVERY: {
        OrderStatusEnum.WAITING_COURIER: [
            OrderStatusEnum.DELIVERY_IN_PROGRESS,
        ],
        OrderStatusEnum.DELIVERY_IN_PROGRESS: [
            OrderStatusEnum.DELIVERED,
        ],
    },
    UserRoleEnum.WAITER: {
        OrderStatusEnum.WAITING_SERVER: [
            OrderStatusEnum.ON_TABLE,
        ],
        OrderStatusEnum.ON_TABLE: [
            OrderStatusEnum.DELIVERED,
        ],
    },
    UserRoleEnum.ADMIN: {
        OrderStatusEnum.CLIENT_NEW: [
            OrderStatusEnum.CLIENT_OPENED,
            OrderStatusEnum.CLIENT_CANCELLED,
        ],
        OrderStatusEnum.CLIENT_OPENED: [
            OrderStatusEnum.PENDING_CONFIRMATION,
            OrderStatusEnum.CLIENT_CANCELLED,
        ],
        OrderStatusEnum.PENDING_CONFIRMATION: [
            OrderStatusEnum.CONFIRMED,
            OrderStatusEnum.CANCELLED,
        ],
        OrderStatusEnum.CONFIRMED: [
            OrderStatusEnum.COOKING,
        ],
        OrderStatusEnum.COOKING: [
            OrderStatusEnum.WAITING_COURIER,
            OrderStatusEnum.WAITING_SERVER,
            OrderStatusEnum.WAITING_PICKUP,
        ],
        OrderStatusEnum.WAITING_COURIER: [
            OrderStatusEnum.DELIVERY_IN_PROGRESS,
        ],
        OrderStatusEnum.WAITING_SERVER: [
            OrderStatusEnum.ON_TABLE,
        ],
        OrderStatusEnum.WAITING_PICKUP: [
            OrderStatusEnum.DELIVERED,
        ],
        OrderStatusEnum.DELIVERY_IN_PROGRESS: [
            OrderStatusEnum.DELIVERED,
        ],
        OrderStatusEnum.ON_TABLE: [
            OrderStatusEnum.DELIVERED,
        ],
        OrderStatusEnum.DELIVERED: [
            OrderStatusEnum.RECEIVED,
        ],
        OrderStatusEnum.RECEIVED: [
            OrderStatusEnum.CONSUMED,
        ],
        OrderStatusEnum.CONSUMED: [
            OrderStatusEnum.RATED,
        ],
    },
}


CLIENT_ONLY_STATUSES = {
    OrderStatusEnum.CLIENT_NEW: [
        OrderStatusEnum.CLIENT_OPENED,
        OrderStatusEnum.CLIENT_CANCELLED,
    ],
    OrderStatusEnum.CLIENT_OPENED: [
        OrderStatusEnum.CLIENT_CANCELLED,
    ],
    OrderStatusEnum.WAITING_PICKUP: [
        OrderStatusEnum.DELIVERED,
    ],
    OrderStatusEnum.DELIVERED: [
        OrderStatusEnum.RECEIVED,
    ],
    OrderStatusEnum.RECEIVED: [
        OrderStatusEnum.CONSUMED,
    ],
    OrderStatusEnum.CONSUMED: [
        OrderStatusEnum.RATED,
    ],
}


STATUS_CHECK_ADMIN_ROLES = {
    status: [
        role for role, statuses in ROLE_STATUS_PERMISSIONS.items() if status in statuses
    ]
    for status in OrderStatusEnum
}
