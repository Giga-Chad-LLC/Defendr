import logging
from fastapi import FastAPI

from server.src.routers import users

try:
    app = FastAPI()
    app.include_router(users.router)

    print("Server started")
except Exception:
    logging.exception("Exception", stack_info=True)
