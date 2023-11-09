from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.directories import DirectoryDto, DirectoryResponse, DirectoriesResponse
from server.src.routers.dependencies.auth import require_auth


router = APIRouter(
    prefix="/directories",
    tags=["directories"],
    responses={
        404: {"detail": "Not found"},
    },
)


# @method: GET
# @route: /directories
# @descr: get all directories
@router.get("/", response_model=DirectoriesResponse, response_description="List of all directories")
def get_directories(connection=Depends(get_connection)):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM directories")
        directories = []

        for row in cursor.fetchall():
            directories.append(DirectoryResponse(
                id=row[0],
                user_id=row[1],
                title=row[2],
                icon=row[3],
            ))

        return DirectoriesResponse(directories=directories)

    finally:
        cursor.close()




# @method: GET
# @route: /directories/{user_id}
# @descr: get directories by user id
@router.get("/{user_id}", response_model=DirectoriesResponse)
def get_directory_by_id(user_id: int, connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        query = "SELECT id, user_id, title, icon FROM directories WHERE user_id = %s"
        cursor.execute(query, (user_id,))

        rows = cursor.fetchall()
        directories = []

        for row in rows:
            directories.append(DirectoryResponse(
                id=row[0],
                user_id=row[1],
                title=row[2],
                icon=row[3],
            ))

        return DirectoriesResponse(directories=directories)
    finally:
        cursor.close()



# @method: POST
# @route: /directories
# @descr: create directory in database
@router.post("/", dependencies=[Depends(require_auth)], response_model=DirectoryResponse)
def create_directory(directory: DirectoryDto, connection=Depends(get_connection)):
    if not directory.user_id or not directory.title or not directory.icon:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be filled")

    cursor = connection.cursor()
    try:
        query = "INSERT INTO directories (user_id, title, icon) VALUES (%s, %s, %s);"

        cursor.execute(query, (directory.user_id, directory.title, directory.icon))

        connection.commit()

        directory_id = cursor.lastrowid

        return DirectoryResponse(
            id=directory_id,
            user_id=directory.user_id,
            title=directory.title,
            icon=directory.icon
        )
    except Exception as err:
        print(err)
        connection.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        cursor.close()
