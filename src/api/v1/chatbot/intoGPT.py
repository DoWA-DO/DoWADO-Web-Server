import os
import re

import openai

# env 파일 불러오기
from dotenv import load_dotenv

load_dotenv()

# 세팅
OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL = "gpt-3.5-turbo"

# 프롬프트 작성 
def post_gpt(system_content, user_content):
    try:
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            # max_tokens=3000,
            stop=None,
            temperature=0.5
        )
        answer = response.choices[0].message.content
        print("gpt 답변: " + answer)
        return answer
    except Exception as e:
        print(e)
        return None
        
def create_prediction_prompt(prompt):
    # "You are a helpful career counseling assistant."
    system_content = "너는 진로 상담사야."
    pre_prompt = "한국어로 답변해줘; 해당 문장을 통해 나올 수 있는 예상 질문을 1개 출력해줘; \n\n"
    answer = post_gpt(system_content, pre_prompt + prompt)
    return answer