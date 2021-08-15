import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import doc, api
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


# configure static and templates file on jinja 2
app = FastAPI(
    title=f"Technical Case",
    description=f"endpoint para subir planilhas para banco de dados relacional Postgres.",
    version=f"0.0.1",
    static_directory="static"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

#import factory builders and initiate
doc.init_app(app)
api.init_app(app, "/api")

#
templates = Jinja2Templates(directory="templates")
#views
@app.get("/", tags=["/view"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
