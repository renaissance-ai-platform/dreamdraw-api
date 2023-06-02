import uvicorn

from dreamdraw_api import config

if __name__ == "__main__":
    uvicorn.run(app="app:app",
    reload=True if config.ENVIRONMENT != "production" else False,
    workers=2,
)