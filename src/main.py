import os
import sys
sys.path.append("..")

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.auth.api import router as auth_router


def create_fast_api_app():
    load_dotenv(find_dotenv(".env"))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        _app = FastAPI(
            default_response_class=ORJSONResponse,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url=None,
            redoc_url=None
        )

    _app.include_router(auth_router, prefix="/api")

    return _app


app = create_fast_api_app()
