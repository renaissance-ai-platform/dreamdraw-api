
from typing import Callable
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dreamdraw_api import config
from dreamdraw_api.api.api import router as api_router

def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        pass
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        pass
    return stop_app

async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)

async def http422_error_handler(_:Request, exc:RequestValidationError) -> JSONResponse:
    return JSONResponse({"errors": exc.errors()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

def create_app() -> FastAPI:
    app = FastAPI(
        redoc_url="/redoc",
        debug=True,
        title="DreamDraw API"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.mount("/images", StaticFiles(directory=config.SAVE_DIR), name="result image")

    app.include_router(api_router, prefix=config.API_PREFIX)

    return app

app = create_app()