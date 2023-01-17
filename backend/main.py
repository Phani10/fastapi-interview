from fastapi import FastAPI
from database import models
from database.database import engine
from routers import user, questions
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(questions.router)
app.include_router(authentication.router)


@app.get("/")
def root():
    return "Hello world!"


origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/resume', StaticFiles(directory='resume'), name='resume')
