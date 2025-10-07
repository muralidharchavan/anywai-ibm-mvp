from routers.score_interview import score_interview
from routers.score_interview import get_llm_score
import logging
from logger_config import setup_logging_to_debug_level, setup_logging_to_info_level
import asyncio

setup_logging_to_info_level()


if __name__ == "__main__":
    asyncio.run(score_interview(301))
    
    # question = "How willing are you to travel between Germany and Switzerland every week?"
    # expected_answer = "Weekly mobility is mandatory"
    # candidate_answer = "So I'm fully comfortable with Monday to Thursday rhythm in Zurich and Fridays I'm back in Berlin. So I have done that for 2 years already and this kind of logistics is no problem for me and it's a second nature, so I can easily deal with that."
    # weightage = 20
    # score_answer = score_answer(question, expected_answer, candidate_answer, weightage)
    # print(f"score_answer: {score_answer}")
