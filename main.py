from fastapi import FastAPI
import heroes
from db import Base, engine
import models   

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(heroes.router)


