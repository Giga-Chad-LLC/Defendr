from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection


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
def get_users(connection=Depends(get_connection)):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = []

        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "email": row[1],
            })

        return users


@router.get("/{user_id}")
def get_user_by_id(user_id: int, connection=Depends(get_connection)):
    with connection.cursor() as cursor:
        query = "SELECT id, email FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))

        row = cursor.fetchone()

        if cursor.rowcount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with id '{user_id}' not found")
        else:
            return {
                "id": row[0],
                "email": row[1],
            }

