from fastapi import APIRouter
from server.src.db.connection import ConnectionManager


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={

        404: {"detail": "Not found"},
    },
)


# @method: GET
# @route: /users
# @descr: get all users
@router.get("/")
def get_users(session):
    manager = ConnectionManager()
    manager.connect()

    with manager.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = []

        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "email": row[1],
            })

        return users

