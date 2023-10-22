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
# @route: /infoboxes/online-service
# @descr: create infobox of type 'ONLINE_SERVICE' in database
@router.post("/online-service", response_model=InfoboxResponse)
def create_online_service_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
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
# @route: /infoboxes/international-passport
# @descr: create infobox of type 'INTERNATIONAL_PASSPORT' in database
@router.post("/international-passport", response_model=InfoboxResponse)
def create_international_passport_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
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
# @route: /infoboxes/bankcard
# @descr: create infobox of type 'BANKCARD' in database
@router.post("/bankcard", response_model=InfoboxResponse)
def create_bankcard_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
    print(infobox.fields)

    user_id = infobox.user_id
    number, cvv, pin = infobox.fields['number'], infobox.fields['cvv'], infobox.fields['pin']
    print(user_id, number, cvv, pin)

    return InfoboxResponse(
        id=1,
        user_id=1,
        directory_id=None,
        icon="icon",
        title="title",
        layout="layout",
        fields={}
    )
