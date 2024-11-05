from fastapi import FastAPI
import uvicorn
from api.casts import casts
from api.db import metadata, database, engine
import os

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get('SERVER_PORT', 8002)), reload=True)