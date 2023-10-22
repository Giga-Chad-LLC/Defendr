from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.directories import DirectoryDto, DirectoryResponse, DirectoriesResponse


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
    directories = []
    return DirectoriesResponse(directories=directories)




# @method: GET
# @route: /directories/{user_id}
# @descr: get directories by user id
@router.get("/{user_id}", response_model=DirectoriesResponse)
def get_directory_by_id(user_id: int, connection=Depends(get_connection)):
    return DirectoriesResponse(directories=[])



# @method: POST
# @route: /directories
# @descr: create directory in database
@router.post("/", response_model=DirectoryResponse)
def create_directory(directory: DirectoryDto, connection=Depends(get_connection)):
    return DirectoryResponse(
        id=-1,
        user_id=-1,
        title="title",
        icon="icon"
    )
