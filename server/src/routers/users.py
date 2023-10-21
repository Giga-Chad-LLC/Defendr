import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.users import UserDto, UserResponse, UsersResponse

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
@router.get("/", response_model=UsersResponse, response_description="List of all users")
def get_users(connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        users = []

        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "email": row[1],
            })

        return UsersResponse(users=users)
    finally:
        cursor.close()



# @method: GET
# @route: /users/{user_id}
# @descr: get user by id
@router.get("/{user_id}", response_model=UserResponse, response_description="User data of user with the same id")
def get_user_by_id(user_id: int, connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        query = "SELECT id, email FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))

        row = cursor.fetchone()

        if cursor.rowcount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with id '{user_id}' not found")
        else:
            return UserResponse(id=row[0], email=row[1])
    finally:
        cursor.close()



# @method: POST
# @route: /users
# @descr: creates user in database
@router.post("/{user_id}", response_model=UserResponse, response_description="User data of inserted user")
def create_user(user: UserDto, connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (user.email, user.password))

        connection.commit()

        user_id = cursor.lastrowid
        return UserResponse(id=user_id, email=user.email)

    except Exception as err:
        connection.rollback()
        raise err
    finally:
        cursor.close()
