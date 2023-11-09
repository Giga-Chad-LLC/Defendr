import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.infoboxes import (
    available_infobox_layouts,
    available_field_types,
    InfoboxDto,
    InfoboxResponse,
    InfoboxesResponse,
)
from server.src.routers.dependencies.auth import require_auth


router = APIRouter(
    prefix="/infoboxes",
    tags=["infoboxes"],
    responses={
        404: {"detail": "Not found"},
    },
)



def retrive_infobox_data_by_id(connection, infobox_id):
    cursor = connection.cursor()
    try:
        query = """
            SELECT
                i.id AS infobox_id,
                i.user_id AS infobox_user_id,
                i.directory_id AS infobox_directory_id,
                i.title AS infobox_title,
                i.icon AS infobox_icon,
                i.layout as infobox_layout,
                f.id AS field_id,
                f.label AS field_label,
                f.type AS field_type,
                tf.value AS text_field_value,
                sf.id AS selection_field_id,
                o.label AS option_label,
                o.selected AS option_selected
            FROM infoboxes i
            INNER JOIN fields f ON i.id = f.infobox_id
            LEFT JOIN text_fields tf ON f.id = tf.field_id AND f.type = 'TEXT'
            LEFT JOIN selection_fields sf ON f.id = sf.field_id AND f.type = 'SELECTION'
            LEFT JOIN options o ON sf.id = o.selection_field_id
            WHERE i.id = %s;
        """

        cursor.execute(query, (infobox_id,))
        rows = cursor.fetchall()

        if cursor.rowcount <= 0:
            raise ValueError(f'Data for infobox with id {infobox_id} not found')

        data = []

        for row in rows:
            response = InfoboxResponse(
                infobox_id=row[0],
                infobox_user_id=row[1],
                infobox_directory_id=row[2],
                infobox_title=row[3],
                infobox_icon=row[4],
                infobox_layout=row[5],
                field_id=row[6],
                field_label=row[7],
                field_type=row[8],
                text_field_value=row[9],
                selection_field_id=row[10],
                option_label=row[11],
                option_selected=row[12],
            )

            data.append(response)

        print(data)
        return data
    finally:
        cursor.close()



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



# @method: GET
# @route: /infoboxes
# @descr: get all infoboxes
@router.get("/", response_model=InfoboxesResponse, response_description="List of all infoboxes")
def get_infoboxes(connection=Depends(get_connection)):
    # TODO: implement
    pass



# @method: GET
# @route: /infoboxes/{infobox_id}
# @descr: get infobox by id
@router.get("/{infobox_id}", response_model=InfoboxResponse, response_description="Infobox data of infobox with the same id")
def get_infobox_by_id(infobox_id: int, connection=Depends(get_connection)):
    # TODO: implement
    pass



# @method: POST
# @route: /infoboxes/online-service
# @descr: create infobox of type 'ONLINE_SERVICE' in database
@router.post("/online-service", dependencies=[Depends(require_auth)], response_model=InfoboxesResponse)
def create_online_service_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
    email, password, url = infobox.fields["email"], infobox.fields["password"], infobox.fields["url"]

    if not email or not password or not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be non-empty")

    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        infobox_id = create_infobox_in_bd(connection, {
            'user_id': infobox.user_id,
            'directory_id': infobox.directory_id,
            'icon': 'online-service',
            'title': 'online-service',
            'layout': available_infobox_layouts['ONLINE_SERVICE']
        })

        fields_data = [
            {
                "infobox_id": infobox_id,
                "label": 'Url',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": url
                }
            },
            {
                "infobox_id": infobox_id,
                "label": 'Email',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": email
                }
            },
            {
                "infobox_id": infobox_id,
                "label": 'Password',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": password
                }
            }
        ]

        for data in fields_data:
            create_infobox_field_in_db(connection, data)

        response = retrive_infobox_data_by_id(connection, infobox_id)
        return InfoboxesResponse(infoboxes=response)

    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))




# @method: POST
# @route: /infoboxes/international-passport
# @descr: create infobox of type 'INTERNATIONAL_PASSPORT' in database
@router.post("/international-passport", dependencies=[Depends(require_auth)], response_model=InfoboxesResponse)
def create_international_passport_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
    name, nationality, number, surname = infobox.fields["name"], infobox.fields["nationality"], infobox.fields["number"], infobox.fields["surname"]

    if not name or not nationality or not number or not surname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be non-empty")

    try:
        infobox_id = create_infobox_in_bd(connection, {
            'user_id': infobox.user_id,
            'directory_id': infobox.directory_id,
            'icon': 'national-passport',
            'title': 'national-passport',
            'layout': available_infobox_layouts['INTERNATIONAL_PASSPORT']
        })

        fields_data = [
            {
                "infobox_id": infobox_id,
                "label": 'Name',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": name
                }
            },
            {
                "infobox_id": infobox_id,
                "label": 'Nationality',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": nationality
                }
            },
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
                "label": 'Surname',
                "required": True,
                "type": available_field_types['text'],
                "properties": {
                    "value": surname
                }
            }
        ]

        for data in fields_data:
            create_infobox_field_in_db(connection, data)

        response = retrive_infobox_data_by_id(connection, infobox_id)
        return InfoboxesResponse(infoboxes=response)

    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))



# @method: POST
# @route: /infoboxes/bankcard
# @descr: create infobox of type 'BANKCARD' in database
@router.post("/bankcard", dependencies=[Depends(require_auth)], response_model=InfoboxesResponse)
def create_bankcard_infobox(infobox: InfoboxDto, connection=Depends(get_connection)):
    print(infobox.fields)
    number, cvv, pin = infobox.fields['number'], infobox.fields['cvv'], infobox.fields['pin']

    if (not number) or (not cvv) or (not pin):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be non-empty")

    try:
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

        response = retrive_infobox_data_by_id(connection, infobox_id)
        return InfoboxesResponse(infoboxes=response)

    except Exception as err:
        msg = str(err)
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
