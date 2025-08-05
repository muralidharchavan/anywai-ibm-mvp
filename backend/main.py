from fastapi import FastAPI
from routers import score_answers
from routers import db_router

app = FastAPI()
app.include_router(score_answers.router)
app.include_router(db_router.router)
