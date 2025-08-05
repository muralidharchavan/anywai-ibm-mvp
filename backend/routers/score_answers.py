from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import os
from dotenv import load_dotenv
import re

load_dotenv()
router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str



@router.post("/score_answers")
async def score_answers(question: str, expected_answer: str, candidate_answer: str, weightage: int):
    try:

        scoring_prompt = f"""System:
            You are an expert technical interviewer. Evaluate the candidate's answer compared to the expected answer.

            - Consider correctness, completeness, clarity, and relevance.
            - Assign a **single overall score out of <weightage>**.
            - Provide **brief feedback (1-2 sentences)** explaining the score.
            - **Do not repeat or restate the question, expected answer, or candidate answer.**
            - Return **only** the score and the feedback.

            ---

            Input:
            Question: {question}
            Expected Answer: {expected_answer}
            Candidate Answer: {candidate_answer}
            Weightage: {weightage}

            ---

            Output format:
            {{
            "score": <score out of {weightage}>,
            "feedback": "<brief reason for the score>"
            }}"""


        watsonx_url = os.getenv("WATSONX_URL")
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        model_id = os.getenv("WATSONX_MODEL_ID")

        credentials = Credentials(
            url=watsonx_url,
            api_key=api_key
        )
        client = APIClient(credentials)

        params = {
            "decoding_method": "greedy",
            "max_new_tokens": 100
        }

        model = ModelInference(
            model_id=model_id,
            api_client=client,
            params=params,
            project_id=project_id,
            space_id=None,
            verify=False
        )

        return model.generate_text(scoring_prompt)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))