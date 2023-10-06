import random
import mysql.connector
from faker import Faker


fake = Faker()
USERS_COUNT = 100
INFOBOXES_COUNT_PER_USER = 10

available_infobox_layouts = [
    'ONLINE_SERVICE',
    'INTERNATIONAL_PASSPORT',
    'BANK_CARD',
    'DRIVING_LICENSE',
    # 'CUSTOM_LAYOUT'
]

available_field_types = {
    "selection": "SELECTION",
    "text": "TEXT"
}


def randint(length: int) -> int:
    length -= 1
    return random.randint(int(10 ** length), int(10 ** (length + 1) - 1))


def insert_selection_field_option(cursor, data) -> int:
    selection_field_option_query = "INSERT INTO options (selection_field_id, label, selected) VALUES (%s, %s, %s)"
    cursor.execute(selection_field_option_query, data)
    return cursor.lastrowid


def insert_selection_field(cursor, data) -> int:
    selection_field_query = "INSERT INTO selection_fields (field_id) VALUES (%s)"
    cursor.execute(selection_field_query, data)
    return cursor.lastrowid


def insert_text_field(cursor, data) -> int:
    text_field_query = "INSERT INTO text_fields (field_id, value) VALUES (%s, %s)"
    cursor.execute(text_field_query, data)
    return cursor.lastrowid


def insert_field(cursor, data) -> int:
    field_query = "INSERT INTO fields (infobox_id, label, required, type) VALUES (%s, %s, %s, %s)"
    cursor.execute(field_query, data)
    return cursor.lastrowid



def insert_online_service_fields(cursor, infobox_id):
    # inserting field with link to the resource
    field_id = insert_field(cursor, (infobox_id, 'Service link', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.uri()))

    # inserting field with email registered on the resource
    field_id = insert_field(cursor, (infobox_id, 'Registered email', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.email()))

    # inserting field with password registered on the resource
    # TODO: there must be another prop in 'available_field_types' called `password`
    field_id = insert_field(cursor, (infobox_id, 'Password', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.password()))



# Note: not all fields present here for simplisity
def insert_international_passport_fields(cursor, infobox_id):
    # series
    field_id = insert_field(cursor, (infobox_id, 'Series', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, randint(2)))

    field_id = insert_field(cursor, (infobox_id, 'Number', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, randint(7)))

    # given names
    field_id = insert_field(cursor, (infobox_id, 'Given names', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.first_name()))

    # surname
    field_id = insert_field(cursor, (infobox_id, 'Surname', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.last_name()))

    # authority
    field_id = insert_field(cursor, (infobox_id, 'Authority', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.address()))

    # date of birth
    # TODO: need 'date' in 'available_field_types'
    field_id = insert_field(cursor, (infobox_id, 'Date of birth', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.date()))



# Note: not all fields present for simplisity
def insert_bank_card_fields(cursor, infobox_id):
    # number
    field_id = insert_field(cursor, (infobox_id, 'Card number', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, randint(19)))

    # CVV
    field_id = insert_field(cursor, (infobox_id, 'CVV', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, randint(3)))

    # holder name
    field_id = insert_field(cursor, (infobox_id, 'Holder', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.name()))



def insert_driving_license_fields(cursor, infobox_id):
    # license id
    field_id = insert_field(cursor, (infobox_id, 'License ID', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, randint(15)))

    # issue date
    field_id = insert_field(cursor, (infobox_id, 'Issue date', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.date()))

    # expirary date
    field_id = insert_field(cursor, (infobox_id, 'Expirary date', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.date()))

    # Holder name
    field_id = insert_field(cursor, (infobox_id, 'Holder', True, available_field_types['text']))
    insert_text_field(cursor, (field_id, fake.name()))

    # vehicle categories: field-> selected_field -> options
    field_id = insert_field(cursor, (infobox_id, 'Vehicle categories', True, available_field_types['selection']))
    selection_field_id = insert_selection_field(cursor, (field_id,))

    for label in ['M', 'A', 'A1', 'B', 'B1', 'C', 'D', 'E']:
        selected = (random.randint(0, 1) == 0)
        insert_selection_field_option(cursor, (selection_field_id, label, selected))



def populate_infoboxes(cursor, users_ids) -> list[int]:
    users_infoboxes_ids_dict: dict[int, list[int]] = {}

    for user_id in users_ids:
        print(f"======= Inserting {INFOBOXES_COUNT_PER_USER} infoboxes for user {user_id} =======")

        inserted_infoboxes_ids: list[int] = []

        for _ in range(INFOBOXES_COUNT_PER_USER):
            index = random.randint(0, len(available_infobox_layouts) - 1)
            infobox_layout = available_infobox_layouts[index]

            insert_infobox_query = """
                INSERT INTO infoboxes (user_id, directory_id, icon, title, layout)
                VALUES (%s, %s, %s, %s, %s)
            """

            infobox_data = (user_id, None, f"{infobox_layout}_ICON", fake.sentence()[:100], infobox_layout)
            cursor.execute(insert_infobox_query, infobox_data)

            infobox_id = cursor.lastrowid

            print(f"Successfully inserted infobox with id {infobox_id} with layout {infobox_layout}")

            # generating appropriate fields for the infobox layout
            if infobox_layout == 'ONLINE_SERVICE':
                insert_online_service_fields(cursor, infobox_id)
            elif infobox_layout == 'INTERNATIONAL_PASSPORT':
                insert_international_passport_fields(cursor, infobox_id)
                pass
            elif infobox_layout == 'BANK_CARD':
                insert_bank_card_fields(cursor, infobox_id)
            elif infobox_layout == 'DRIVING_LICENSE':
                insert_driving_license_fields(cursor, infobox_id)

            print("Successfully inserted infobox fields\n")
            inserted_infoboxes_ids.append(infobox_id)

        users_infoboxes_ids_dict[user_id] = inserted_infoboxes_ids
        print("\n")

    return users_infoboxes_ids_dict


def populate_users(cursor) -> list[int]:
    inserted_users_ids: list[int] = []
    # Create users
    insert_user_query = "INSERT INTO users (email, password) VALUES (%s, %s)"

    for _ in range(USERS_COUNT):
        user_data = (fake.email(), fake.password())
        cursor.execute(insert_user_query, user_data)

        user_id = cursor.lastrowid
        inserted_users_ids.append(user_id)

    print(f"Successfully inserted {USERS_COUNT} users into database")
    return inserted_users_ids



# MySQL connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123",
    "database": "defendr",
}

# Create a connection to the MySQL server
connection = mysql.connector.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # insert users into db
        users_ids: list[int] = populate_users(cursor)
        infoboxes_ids_per_user_id_dict: dict[int, list[int]] = populate_infoboxes(cursor, users_ids)
        connection.commit()
        print("Data inserted successfully!")
        print(infoboxes_ids_per_user_id_dict)

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")
