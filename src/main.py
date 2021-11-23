import os
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.openapi.utils import get_openapi

from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import Response
from starlette.responses import FileResponse


app = FastAPI(title="Container Python Fastapi Template", version="0.1",
              docs_url="/docs", redoc_url="/redoc")

app.add_middleware(GZipMiddleware, minimum_size=1000)

log_level = os.environ.get('LOG_LEVEL', 'warn')
debug_enable = os.environ.get('DEBUG', False)

favicon_path = "../favicon.ico"


@app.on_event("startup")
async def on_app_start():
    logger.info("Startup")


@app.on_event("shutdown")
async def on_app_shutdown():
    logger.info("Shutdown")


@app.get('/')
def index():
    return {
        "message": "Hello world."
    }


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/home")
async def home():
    return Response("This is your Home")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Container Python Fastapi Template",
        version="0.0.1",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.webera.com/wp-content/uploads/elementor/thumbs/webera-light-1-pcqt8fbgy24nm41xbqqpvi0yu9jkjirq2lr3htt2ro.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, log_level=log_level, host="0.0.0.0",
                port=8080, reload=True, debug=debug_enable)
