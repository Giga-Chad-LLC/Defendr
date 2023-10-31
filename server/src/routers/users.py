import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.users import (
    UserDto,
    UserResponse,
    UsersResponse,
    UserInfoboxCountResponse,
    UsersInfoboxCountResponse,
)
from server.src.routers.models.infoboxes import available_infobox_layouts



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
# @route: /users/single/{user_id}
# @descr: get user by id
@router.get("/single/{user_id}", response_model=UserResponse, response_description="User data of user with the same id")
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
# @descr: create user in database
@router.post("/", response_model=UserResponse, response_description="User data of inserted user")
def create_user(user: UserDto, connection=Depends(get_connection)):
    if user.email == "" or user.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be non-empty")

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



# @method: GET
# @route: /users/layouts
# @descr: return count of infoboxes with the provided layout for all users
@router.get("/layouts", response_model=UsersInfoboxCountResponse,
            response_description="Count of infoboxes with the provided layout for all users")
def get_users_infobox_count_by_layout(layout: str, connection=Depends(get_connection)):

    if layout not in available_infobox_layouts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Layout must be one of {', '.join(available_infobox_layouts.values())}, got '{layout}'")

    cursor = connection.cursor()
    try:
        query = """
            SELECT
                u.id AS user_id,
                i.layout AS infobox_layout,
                COUNT(i.id) AS infobox_count
            FROM users u
            LEFT JOIN infoboxes i ON u.id = i.user_id
            WHERE i.layout = %s
            GROUP BY u.id, i.layout
            ORDER BY user_id, infobox_layout
        """

        cursor.execute(query, (layout,))

        rows = cursor.fetchall()

        data = []
        for (user_id, infobox_layout, infobox_count) in rows:
            data.append(UserInfoboxCountResponse(
                user_id=user_id,
                infobox_layout=infobox_layout,
                infobox_count=infobox_count
            ))

        return UsersInfoboxCountResponse(data=data)
    finally:
        cursor.close()




# @method: GET
# @route: /users/top
# @descr: return top N users that have the maximum number of infoboxes of the provided layout
@router.get("/top", response_model=UsersInfoboxCountResponse,
            response_description="Top 5 users that have the maximum number of infoboxes of the provided layout")
def get_top_users_with_max_infobox_count_by_layout(layout: str, limit: int, connection=Depends(get_connection)):

    if layout not in available_infobox_layouts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Layout must be one of {', '.join(available_infobox_layouts.values())}, got '{layout}'")

    if limit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Limit must be positive number, got '{limit}'")

    cursor = connection.cursor()
    try:
        query = """
            SELECT user_id, infobox_layout, infobox_count
            FROM (
                SELECT
                    u.id AS user_id,
                    u.email AS user_email,
                    i.layout AS infobox_layout,
                    COUNT(i.id) AS infobox_count
                FROM users u
                LEFT JOIN infoboxes i ON u.id = i.user_id AND i.layout = %s
                GROUP BY u.id, u.email
                ORDER BY infobox_count DESC
                LIMIT %s
            ) AS top_users;
        """

        cursor.execute(query, (layout, limit))

        rows = cursor.fetchall()

        data = []
        for (user_id, infobox_layout, infobox_count) in rows:
            data.append(UserInfoboxCountResponse(
                user_id=user_id,
                infobox_layout=(layout if (infobox_layout is None) else infobox_layout),
                infobox_count=infobox_count
            ))

        return UsersInfoboxCountResponse(data=data)
    finally:
        cursor.close()
