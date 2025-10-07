import logging
from fastapi import FastAPI
from routers import db_router
from routers import score_interview
from logger_config import setup_logging_to_debug_level

setup_logging_to_debug_level()
app = FastAPI()
app.include_router(db_router.router)
app.include_router(score_interview.router)

@app.get("/")
def read_root():
    logging.debug("Anywai UDAO backend app is up and running")
    return {"status": "ok", "message": "Anywai UDAO backend app is up and running"}
