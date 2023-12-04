import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from server.src.routers import users, infoboxes, directories, search, geo

try:
    app = FastAPI()

    # required for the CORS pocilies
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Access-Control-Allow-Origin"]
    )
    # Middleware to handle the proxy headers and get the client's real IP address
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    app.include_router(users.router)
    app.include_router(infoboxes.router)
    app.include_router(directories.router)
    app.include_router(search.router)
    app.include_router(geo.router)

    print("Server started")
except Exception:
    logging.exception("Exception", stack_info=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8347)
