
from datetime import datetime
from fastapi import (APIRouter, Response)

from dreamdraw_api.api.generate.generate import generate_api
from dreamdraw_api.api.users.users import users_api

router = APIRouter()

async def index():
    ''' ALB check '''
    current_time = datetime.utcnow()
    msg = f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
    return Response(msg)

router.add_api_route("/", index, status_code=200, methods=["GET"])
router.add_api_route("/health", index, status_code=200, methods=["GET"])

router.include_router(generate_api, tags=["generate"], prefix="/generate")
router.include_router(users_api, tags=["users"], prefix="/users")

