import logging

from fastapi import APIRouter

from app.dependencies import TaxiCrudDep
from app.schemas.taxi import TaxiPostRequest, TaxiPostResponse, TaxiNotifyMessage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/taxi",
    tags=["taxi"],
)


@router.get(
    r"/",
    response_model=TaxiPostResponse,
)
async def taxi_list(crud: TaxiCrudDep):
    items = await crud.get_all()
    return items


@router.post(
    r"/",
    response_model=TaxiPostResponse,
)
async def create_taxi(
    request_body: TaxiPostRequest,
    crud: TaxiCrudDep,
) -> TaxiPostResponse:
    item = await crud.create_taxi(request_body)
    return TaxiPostResponse(id=item.id)


# @router.post(r"/{id_}")
# def notify_taxi(id_:str, data: TaxiNotifyMessage) -> str:
#     url = ...  # urljoin(TAXI_DB[id_], "message")
#     logger.info(f"Sending request to taxi, url: {url}")
#     httpx.post(url, json={"message": data.message})
#     return "ok"
