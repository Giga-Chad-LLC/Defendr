import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, status
from server.src.db.connection import get_connection
from server.src.routers.models.search import SearchResult, SearchResultsResponse


router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={
        404: {"detail": "Not found"},
    },
)


# @method: GET
# @route: /search/user-id
# @descr: get user ids that match the provided query
@router.get("/user-id", response_model=SearchResultsResponse, response_description="List of user ids that match the provided query")
def search_user_ids(term: str, connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM users")
        results = []

        for row in cursor.fetchall():
            id = str(row[0])
            if term in id:
                results.append(SearchResult(label=id, value=id))

        return SearchResultsResponse(results=results)

    except mysql.connector.Error as error:
        print(error)
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        cursor.close()


# @method: GET
# @route: /search/user-email
# @descr: get user emails that match the provided query
@router.get("/user-email", response_model=SearchResultsResponse, response_description="List of user emails that match the provided query")
def search_user_emails(term: str, connection=Depends(get_connection)):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT email FROM users")
        results = []

        for row in cursor.fetchall():
            email = row[0]
            if term in email:
                results.append(SearchResult(label=email, value=email))

        return SearchResultsResponse(results=results)

    except mysql.connector.Error as error:
        print(error)
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        cursor.close()
