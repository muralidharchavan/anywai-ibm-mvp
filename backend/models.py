from pydantic import BaseModel

class CandidateAnswer(BaseModel):
    answer_id: str
    interview_id: str
    question_id: str
    response_text: str
    score: float = 0.0
    ai_comments: str | None = None
