from fastapi import FastAPI
from routers import db_router
from routers import score_interview

app = FastAPI()
app.include_router(db_router.router)
app.include_router(score_interview.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Anywai UDAO backend app is up and running"}
