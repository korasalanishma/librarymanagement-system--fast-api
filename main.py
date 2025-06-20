from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from app.api.users import user_routes


app = FastAPI()

app.include_router(user_routes)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs/")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API for Library Management System",
        version="1.0.0",
        description="This is an API for Library management system Developed with FastAPI, Python and MongoDB",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://yourlogo.com/logo.png",
        "altText": "Your Logo",
    }
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
