from fastapi import FastAPI,status,Response
from fastapi.staticfiles import StaticFiles
from core import engine, Base,auth_router

from fastapi.middleware.cors import CORSMiddleware


import routers

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")

Base.metadata.create_all(engine)


app.include_router(auth_router)
app.include_router(routers.category)
app.include_router(routers.banner_router)
app.include_router(routers.subcategor)
app.include_router(routers.searchpro)
app.include_router(routers.info)
# app.include_router(routers.exam_router)
# app.include_router(routers.question_router)