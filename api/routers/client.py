from fastapi import APIRouter, Depends

from api.dependencies import auth
from schemas import ClientResponseSchema

router = APIRouter(prefix="/client", tags=["Client"])


@router.get(path="/me")
async def get_me(
    current_client: ClientResponseSchema = Depends(dependency=auth.get_current_client),
) -> ClientResponseSchema:
    return current_client
