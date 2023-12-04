import requests
from fastapi import APIRouter, Request, HTTPException, status
from server.src.routers.models.geo import GeoDto, GeoResponse



router = APIRouter(
    prefix="/geo",
    tags=["geo"],
    responses={
        404: {"detail": "Not found"},
    },
)


# @method: GET
# @route: /geo/position
# @descr: Provides geo position coordinates of the IP of the request
@router.get("/position", response_model=GeoResponse, response_description="Provides geo position coordinates of the IP of the request")
def get_geo_position(request: Request):
    client_ip = request.client.host
    response = requests.get(f"https://ipinfo.io/{client_ip}?token=77e30d78913b91")

    if response.status_code == 200:
        data = response.json()

        if "bogon" in data and data["bogon"] is True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot derive location from API of your IP address '{client_ip}'")
        else:
            latitude, longitude = data["loc"].split(',')
            return GeoResponse(geo=GeoDto(latitude=float(latitude), longitude=float(longitude)), ip=client_ip)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not request API to get location details")
