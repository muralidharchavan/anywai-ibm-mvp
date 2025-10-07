from fastapi import APIRouter, HTTPException
from .db_router import prepare_llm_input_data, update_score, update_total_score
from .transcriber import convert_video_to_text
import json
from pydantic import BaseModel
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import os
from dotenv import load_dotenv
import re
import logging


load_dotenv()
router = APIRouter()


def extract_json_from_response(llm_response: str) -> dict:
    try:
        # Extract the JSON part using a regular expression
        match = re.search(r'{.*}', llm_response, re.DOTALL)
        if match:
            json_str = match.group(0)
            logging.debug(f"llm_response: {json_str}")
            return json.loads(json_str)
        else:
            logging.error(f"Error: {llm_response}")
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

        logging.debug(f"score_answer: {(score_answer)}")
        return score_answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_scores_in_db(llm_input_data: dict, interview_id: int):
    try:

        # results = {}
        # all_qtns_scores = []
        total_score = 0
        total_weightage = 0
        # qtn_sl_no = 1
        for answer in llm_input_data:
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

            # all_qtns_scores.append({
            #     "question_id": answer["question_id"],
            #     "weightage": answer["weightage"],
            #     "answer_id": answer["answer_id"],
            #     "interview_id": interview_id,
            #     **result
            # })

            # Update database
            update_score(interview_id, answer["answer_id"], result["score"], result["feedback"])

        # results["total_score"] = total_score
        # results["total_weightage"] = total_weightage
        # results["all_qtns_scores"] = all_qtns_scores

        update_total_score(interview_id, total_score)

        return {"message": f"Interview with id {interview_id} is scored and database is updated"}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/score_interview")
async def score_interview(interview_id: int):
    logging.info("\n" * 5)
    logging.info(f"Processing started for interview_id: {interview_id}")
    try:
        # For the interview id, convert video to text for each question/video and save the text in database
        response = await convert_video_to_text(interview_id)
        logging.info(f"Transcription of all videos of interview_id: {interview_id} are processed and updated to database.")

        # Prepare imput data for invoking LLM
        llm_input_data = prepare_llm_input_data(interview_id)
        logging.info("LLM input data is prepared for interview_id: {interview_id}")
        logging.debug(f"LLM input data: {llm_input_data}")

        llm_scores = update_scores_in_db(llm_input_data, interview_id)
        logging.info("Scores by LLM are updated to database for interview_id: {interview_id}")
        logging.debug(f"llm_scores -> {llm_scores}")
        return llm_scores

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
