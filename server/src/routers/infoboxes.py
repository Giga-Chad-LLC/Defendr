from fastapi import APIRouter, Depends, HTTPException, status
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


available_infobox_layouts = {
    "ONLINE_SERVICE": 'ONLINE_SERVICE',
    "INTERNATIONAL_PASSPORT": 'INTERNATIONAL_PASSPORT',
    "BANK_CARD": 'BANK_CARD',
}

available_field_types = {
    "selection": "SELECTION",
    "text": "TEXT"
}


def create_infobox_in_bd(connection, data):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO infoboxes (user_id, directory_id, icon, title, layout) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (data['user_id'], data['directory_id'], data['icon'], data['title'], data['layout']))
        connection.commit()

        infobox_id = cursor.lastrowid
        return infobox_id
    except Exception as err:
        connection.rollback()
        raise err
    finally:
        cursor.close()


def create_infobox_field_in_db(connection, data):
    cursor = connection.cursor()
    try:
        if data['type'] == available_field_types['text']:
            # insert field into db
            field_query = 'INSERT INTO fields (infobox_id, label, required, type) VALUES (%s, %s, %s, %s)'
            cursor.execute(field_query, (data['infobox_id'], data['label'], data['required'], data['type']))

            field_id = cursor.lastrowid
            value = data['properties']['value']

            # insert text field into db
            text_field_query = 'INSERT INTO text_fields (field_id, value) VALUES (%s, %s)'
            cursor.execute(text_field_query, (field_id, value))

            connection.commit()
        elif data['type'] == available_field_types['selection']:
            # TODO: implement
            raise RuntimeError(f"Not implemented for type '{available_field_types['selection']}'")
        else:
            raise ValueError(f"Unknown field type '{data['type']}'")

    except Exception as err:
        connection.rollback()
        raise err
    finally:
        cursor.close()


# @method: POST
# @route: /infoboxes/bankcard
# @descr: create infobox of type 'BANKCARD' in database
@router.post("/bankcard", response_model=InfoboxResponse)
def create_bankcard_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
    print(infobox.fields)
    number, cvv, pin = infobox.fields['number'], infobox.fields['cvv'], infobox.fields['pin']

    if (not number) or (not cvv) or (not pin):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be non-empty")

    infobox_id = create_infobox_in_bd(connection, {
        'user_id': infobox.user_id,
        'directory_id': infobox.directory_id,
        'icon': 'bankcard-icon',
        'title': 'bankcard',
        'layout': available_infobox_layouts['BANK_CARD']
    })

    fields_data = [
        {
            "infobox_id": infobox_id,
            "label": 'Number',
            "required": True,
            "type": available_field_types['text'],
            "properties": {
                "value": number
            }
        },
        {
            "infobox_id": infobox_id,
            "label": 'CVV',
            "required": True,
            "type": available_field_types['text'],
            "properties": {
                "value": cvv
            }
        },
        {
            "infobox_id": infobox_id,
            "label": 'PIN',
            "required": True,
            "type": available_field_types['text'],
            "properties": {
                "value": pin
            }
        }
    ]

    for data in fields_data:
        create_infobox_field_in_db(connection, data)

    return InfoboxResponse(
        id=infobox_id,
        user_id=infobox.user_id,
        directory_id=infobox.directory_id,
        icon="icon",
        title="title",
        layout="layout",
        fields={}
    )
