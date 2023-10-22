import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.src.routers import users, infoboxes, directories

try:
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(infoboxes.router)
    app.include_router(directories.router)

    # required for the CORS pocilies
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Access-Control-Allow-Origin"]
    )

    print("Server started")
except Exception:
    logging.exception("Exception", stack_info=True)
