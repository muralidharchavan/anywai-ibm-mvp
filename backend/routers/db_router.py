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

# @router.get("/db")
# def get_data():
#     try:
#         response = supabase.table("questions").select("*").execute()
#         return JSONResponse(content=jsonable_encoder(response.data))
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/dashboard_data")
def get_dashboard_data():
    try:
        response = supabase.table("interviews").select("status, interview_id, candidates(full_name, candidate_id), interview_templates(template_name, template_id)").execute()
        flat_data = [
            {
                "full_name": row["candidates"]["full_name"],
                "template_name": row["interview_templates"]["template_name"],
                "status": row["status"],
                "interview_id": row["interview_id"],
                "candidate_id": row["candidates"]["candidate_id"],
                "template_id": row["interview_templates"]["template_id"]
            }
            for row in response.data
        ]      
        return JSONResponse(content=jsonable_encoder(flat_data))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/interview_data")
# def get_interview_data(interview_id: int):
#     try:
#         print(f"Getting data for {interview_id}")
#         response = supabase \
#             .from_("candidate_answers") \
#             .select("interview_id", "question_id", "answer_id", "response_text") \
#             .eq("interview_id", interview_id) \
#             .execute()
    
#         return response.data
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/get_data_for_scoring")
def get_llm_input_data(interview_id: int):
    try:
        # Step 1: Get candidate_answers for interview_id
        answers_resp = supabase \
            .from_("candidate_answers") \
            .select("question_id, response_text, answer_id") \
            .eq("interview_id", interview_id) \
            .execute()

        # Step 2: Collect all unique question_ids
        question_ids = [ans["question_id"] for ans in answers_resp.data]

        # Step 3: Fetch corresponding questions
        questions_resp = supabase \
            .from_("questions") \
            .select("question_id, question_text, expected_answer, weightage") \
            .in_("question_id", question_ids) \
            .execute()

        # Step 4: Join the data manually
        questions_map = {q["question_id"]: q for q in questions_resp.data}

        result = []
        for ans in answers_resp.data:
            q = questions_map.get(ans["question_id"])
            if q:
                result.append({
                    "question_id": q["question_id"],
                    "question_text": q["question_text"],
                    "expected_answer": q["expected_answer"],
                    "response_text": ans["response_text"],
                    "weightage": q["weightage"],
                    "answer_id": ans["answer_id"]
                })

        # # Step 5: Print final result
        # for row in result:
        #     print(row)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

