import os
import sys
sys.path.append("..")

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from src.auth.api import router as auth_router
from src.structure.api import router as structure_router


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
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(structure_router)
    _app.include_router(router, prefix="/api")

    return _app


app = create_fast_api_app()
