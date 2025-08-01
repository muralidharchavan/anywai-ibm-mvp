from fastapi import FastAPI
from routers import candidates

app = FastAPI()
app.include_router(candidates.router)
