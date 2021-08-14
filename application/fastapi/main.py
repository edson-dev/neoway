import uvicorn
from fastapi import FastAPI
from routes import doc, api

import os


# configure static and templates file on jinja 2
app = FastAPI(
    title=f"teste title",
    description=f"teste description",
    version=f"teste version",
    static_directory="static"
)
doc.init_app(app)
api.init_app(app, "/api")

@app.get("/", tags=["/view"])
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
