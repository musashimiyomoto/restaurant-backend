from fastapi import APIRouter

from .auth import router as auth_router
from .category import router as category_router
from .client import router as client_router
from .delivery import router as delivery_router
from .dish import router as dish_router
from .image import router as image_router
from .order import router as order_router
from .schedule import router as schedule_router
from .statistics import router as statistics_router
from .user import router as user_router

router = APIRouter(prefix="/admin")

router.include_router(router=auth_router)
router.include_router(router=category_router)
router.include_router(router=dish_router)
router.include_router(router=image_router)
router.include_router(router=order_router)
router.include_router(router=schedule_router)
router.include_router(router=user_router)
router.include_router(router=client_router)
router.include_router(router=statistics_router)
router.include_router(router=delivery_router)

__all__ = ["router"]
