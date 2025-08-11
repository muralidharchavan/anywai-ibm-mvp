from fastapi import APIRouter, HTTPException
from .db_router import get_llm_input_data
import json
from pydantic import BaseModel
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import os
from dotenv import load_dotenv
import re

load_dotenv()
router = APIRouter()


def extract_json_from_response(llm_response: str) -> dict:
    try:
        # Extract the JSON part using a regular expression
        match = re.search(r'{.*}', llm_response, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            print(f"llm_response: {llm_response}")
            raise ValueError("No JSON found in LLM response response.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")
    

def get_llm_score(question: str, expected_answer: str, candidate_answer: str, weightage: int):
    try:

        scoring_prompt = f"""System:
            You are an expert technical interviewer. Evaluate the candidate's answer compared to the expected answer.

            - Consider correctness, completeness, clarity, and relevance.
            - Assign a **single overall score out of <weightage>**.
            - Provide **brief feedback (1-2 sentences)** explaining the score.
            - **Do not repeat or restate the question, expected answer, or candidate answer.**
            - Return **only** the score and the feedback in the following JSON format:
                {{
                    "score": <score out of {weightage}>,
                    "feedback": "<brief reason for the score>"
                }}
            - Do not include any special tokens, such as `<|eom_id|>`, in the output.
            ---

            Input:
            Question: {question}
            Expected Answer: {expected_answer}
            Candidate Answer: {candidate_answer}
            Weightage: {weightage}

            """

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
            "max_new_tokens": 300
        }

        model = ModelInference(
            model_id=model_id,
            api_client=client,
            params=params,
            project_id=project_id,
            space_id=None,
            verify=False
        )

        score_answer = model.generate_text(scoring_prompt)
        score_answer = score_answer.replace("<|eom_id|>", "").strip()

        # print(f"score_answer: {(score_answer)}")
        return score_answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_scores(interview_id: int):
    try:
        scoring_input_data = get_llm_input_data(interview_id)

        results = {}
        all_qtns_scores = []
        total_score = 0
        total_weightage = 0
        # qtn_sl_no = 1
        for answer in scoring_input_data:
            # print(f"Scoring for question serial number: {qtn_sl_no}")
            # qtn_sl_no = qtn_sl_no + 1
            llm_response = get_llm_score(
                question=answer["question_text"],
                expected_answer=answer["expected_answer"],
                candidate_answer=answer["response_text"],
                weightage=answer["weightage"]
            )

            result = extract_json_from_response(llm_response)

            total_score = total_score + result["score"]
            total_weightage = total_weightage + answer["weightage"]

            all_qtns_scores.append({
                "question_id": answer["question_id"],
                "weightage": answer["weightage"],
                "answer_id": answer["answer_id"],
                **result
            })

        results["total_score"] = total_score
        results["total_weightage"] = total_weightage
        results["all_qtns_scores"] = all_qtns_scores

        # Update database


        # return {"results": results}
        print(f"Results: {json.dumps(results)}")

        return {"message": "Will get back"}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/score_interview")
def score_interview(interview_id: int):
    try:
        scoring_input_data = get_llm_input_data(interview_id)

        results = {}
        all_qtns_scores = []
        total_score = 0
        total_weightage = 0
        # qtn_sl_no = 1
        for answer in scoring_input_data:
            # print(f"Scoring for question serial number: {qtn_sl_no}")
            # qtn_sl_no = qtn_sl_no + 1
            llm_response = get_llm_score(
                question=answer["question_text"],
                expected_answer=answer["expected_answer"],
                candidate_answer=answer["response_text"],
                weightage=answer["weightage"]
            )

            result = extract_json_from_response(llm_response)

            total_score = total_score + result["score"]
            total_weightage = total_weightage + answer["weightage"]

            all_qtns_scores.append({
                "question_id": answer["question_id"],
                "weightage": answer["weightage"],
                "answer_id": answer["answer_id"],
                **result
            })

        results["total_score"] = total_score
        results["total_weightage"] = total_weightage
        results["all_qtns_scores"] = all_qtns_scores

        # Update database


        # return {"results": results}
        print(f"Results: {json.dumps(results)}")

        return {"message": "Will get back"}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
