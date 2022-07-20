from fastapi.openapi.docs import get_swagger_ui_html

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import router

app = FastAPI(docs_url=None, redoc_url=None, openapi_url="/openapi.json")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# region Custom Open Api
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(title="User Login API", version="20220629", description="Login API List", routes=app.routes)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/", include_in_schema=False)
async def homepage():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="User Login API",
                               oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                               swagger_js_url="/static/swagger-ui-bundle.js", swagger_css_url="/static/swagger-ui.css",
                               swagger_favicon_url="/static/favicon.png")


app.openapi = custom_openapi

app.include_router(router, tags=['API List'])

# endregion
