import logging
import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException
import httpx  # async HTTP client
from .db_router import get_all_video_file_names, add_transcript_to_db
from .vid_to_stt import transcribe_endpoint

# In the problem module:
logger = logging.getLogger("udao.transcriber")
logger.setLevel(logging.DEBUG)  # show debug logs for this module only

async def get_transcript_text(ans_vid_filename: str) -> str:
    """
    Calls internal transcribe function (sync) to get text.
    """
    try:
        data = transcribe_endpoint(ans_vid_filename)
        return data.get("transcript", "")
    except Exception as e:
        logger.error(f"Error fetching transcript for {ans_vid_filename}: {e}")
        return ""
        

async def process_single_answer(answer_id: int, interview_id: int, file_name: str):
    """
    Handles one transcript: fetch → extract → update
    """
    logger.debug(f"Processing transcript: {file_name}")

    try: 
        transcript_text = await get_transcript_text(file_name)
        logger.debug(f"transcript_text for file {file_name} is {transcript_text}")

        if not transcript_text.strip():
            logger.debug(f"⚠️ No text extracted for {file_name}")
            return {"answer_id": answer_id, "status": "no_text"}

        return add_transcript_to_db(interview_id, answer_id, transcript_text)

    except Exception as e:
        logger.error(f"Failed to update answer_id={answer_id}: {e}")
        return {"answer_id": answer_id, "status": f"error: {e}"}
    

async def convert_video_to_text(interview_id: int):
    logger.info("Converting interview videos to text")
    """
    1️⃣ Fetch all ans_vid_filename for a given interview_id
    2️⃣ Extract text using API
    3️⃣ Update response_text in Supabase
    """

    # Step 1: Fetch from Supabase
    file_names_response = get_all_video_file_names(interview_id)
    logger.debug(f"All video file names: {file_names_response}")

    file_names = file_names_response.data
    if not file_names:
        logger.warning("No video files found for interview_id: {interview_id}")
        raise HTTPException(status_code=404, detail="No transcripts found for this interview_id")
    logger.debug(f"Found {len(file_names)} transcript entries for interview_id={interview_id}")

    # Step 2: Process transcripts concurrently
    import asyncio

    tasks = []
    for file in file_names:
        file_name = file.get("ans_vid_filename")
        answer_id = file.get("answer_id")

        if not file_name:
            logger.debug(f"Skipping answer_id={answer_id} (no ans_vid_filename)")
            continue

        tasks.append(process_single_answer(answer_id, interview_id, file_name))

    logger.debug("Data prepped to run all video to text files parallelly")
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {"status": "completed", "results": results}
