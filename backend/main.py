import logging
from fastapi import FastAPI
from routers import db_router
from routers import score_interview
from logger_config import setup_logging_to_debug_level
from fastapi.middleware.cors import CORSMiddleware

setup_logging_to_debug_level()
app = FastAPI()
app.include_router(db_router.router)
app.include_router(score_interview.router)



# List of origins allowed to make requests to this server
origins = [
    "http://localhost:3000",  # React local
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # or ["*"] to allow all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],             # GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],             # Allow all headers
)

@app.get("/")
def read_root():
    logging.debug("Anywai UDAO backend app is up and running")
    return {"status": "ok", "message": "Anywai UDAO backend app is up and running"}
