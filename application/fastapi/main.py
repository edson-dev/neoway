import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import doc, api

import os


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

#views
@app.get("/", tags=["/view"])
async def index():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
