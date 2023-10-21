from fastapi import APIRouter, Depends
from server.src.db.connection import get_connection
from server.src.routers.models.infoboxes import InfoboxDto, InfoboxResponse, InfoboxesResponse


router = APIRouter(
    prefix="/infoboxes",
    tags=["infoboxes"],
    responses={
        404: {"detail": "Not found"},
    },
)


# @method: GET
# @route: /infoboxes
# @descr: get all infoboxes
@router.get("/", response_model=InfoboxesResponse, response_description="List of all infoboxes")
def get_infoboxes(connection=Depends(get_connection)):
    # TODO: implement
    return InfoboxesResponse(infoboxes=[
        InfoboxResponse(
            id=1,
            user_id=1,
            directory_id=None,
            icon="icon",
            title="title",
            layout="layout"
        )
    ])

# @method: GET
# @route: /infoboxes/{infobox_id}
# @descr: get infobox by id
@router.get("/{infobox_id}", response_model=InfoboxResponse, response_description="Infobox data of infobox with the same id")
def get_infobox_by_id(infobox_id: int, connection=Depends(get_connection)):
    # TODO: implement
    return InfoboxResponse(
        id=1,
        user_id=1,
        directory_id=None,
        icon="icon",
        title="title",
        layout="layout"
    )


# @method: POST
# @route: /infoboxes
# @descr: create infobox in database
@router.post("/", response_model=InfoboxResponse, response_description="Infobox data of infobox with the same id")
def get_infobox_by_id(infobox: InfoboxDto, connection=Depends(get_connection)):
    # TODO: implement
    return InfoboxResponse(
        id=1,
        user_id=1,
        directory_id=None,
        icon="icon",
        title="title",
        layout="layout"
    )
