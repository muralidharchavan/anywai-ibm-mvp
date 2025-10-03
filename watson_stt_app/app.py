import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import ibm_boto3
from ibm_botocore.client import Config
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Load COS credentials from environment
COS_APIKEY = os.getenv("COS_APIKEY")
COS_RESOURCE_ID = os.getenv("COS_RESOURCE_ID")
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_BUCKET = os.getenv("COS_BUCKET")
COS_FILE_KEY = os.getenv("COS_FILE_KEY")
COS_AUTH_ENDPOINT = os.getenv("COS_AUTH_ENDPOINT")

# Load STT credentials from environment
STT_APIKEY = os.getenv("STT_APIKEY")
STT_URL = os.getenv("STT_URL")

AUDIO_FILE = "extracted_audio.wav"

class TranscriptionRequest(BaseModel):
    file_key: str

def download_video(file_key, local_filename):
    cos = ibm_boto3.client(
        "s3",
        ibm_api_key_id=COS_APIKEY,
        ibm_service_instance_id=COS_RESOURCE_ID,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    try: 
        cos.download_file(Bucket=COS_BUCKET, Key=file_key, Filename=local_filename)
        print(f"✅ Downloaded video from COS: {file_key}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_audio(input_video, output_audio):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Audio extracted → {output_audio}")

def transcribe_audio(audio_path):
    authenticator = IAMAuthenticator(STT_APIKEY)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(STT_URL)

    with open(audio_path, 'rb') as audio_file:
        result = stt.recognize(
            audio=audio_file,
            content_type='audio/wav',
            model='en-US_BroadbandModel',
            smart_formatting=True
        ).get_result()

    transcripts = [r['alternatives'][0]['transcript'] for r in result.get('results', [])]
    return " ".join(transcripts)

@app.get("/")
def home():
    return {"message": "FastAPI STT app is running!"}

@app.post("/transcribe")
def transcribe_endpoint(request: TranscriptionRequest):
    file_key = request.file_key
    local_video = file_key  # save with same name

    try:
        download_video(file_key, local_video)
        extract_audio(local_video, AUDIO_FILE)
        transcript = transcribe_audio(AUDIO_FILE)
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 👇 Add this so you can run with `python app.py`
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)