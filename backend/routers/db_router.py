from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import traceback

load_dotenv()

# Replace with your actual Supabase URL and KEY or use environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

router = APIRouter()

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.get("/db")
def get_data():
    try:
        response = supabase.table("questions").select("*").execute()
        return JSONResponse(content=jsonable_encoder(response.data))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/dashboard_data")
def get_dashboard_data():
    try:
        response = supabase.table("interviews").select("status, candidates(full_name), interview_templates(template_name)").execute()
        flat_data = [
            {
                "full_name": row["candidates"]["full_name"],
                "template_name": row["interview_templates"]["template_name"],
                "status": row["status"]
            }
            for row in response.data
        ]      
        return JSONResponse(content=jsonable_encoder(flat_data))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))