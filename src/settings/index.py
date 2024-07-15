"""
생성 AI index 설정(초기화) 모듈
"""
# import os
# import openai
# from src.settings.dto import BaseDTO
# from typing import NewType


# openai.api_key = os.environ['OPENAI_API_KEY'] = env.OPENAI_API_KEY
# ChatID = NewType('ChatID', str)

# class ChatOptions(BaseDTO):
#     model_name : str = "gpt-3.5-turbo=1106" # text-davinci-003, gpt-3.5-turbo, gpt-3.5-turbo-1106
#     temperature: int = 0
#     context_window: int = 4096 # 16385, 모델이 한 번에 처리할 수 있는 최대 토큰 수, 최대 컨텍스트 길이 재조사 필요
#     max_token: int = 1024 #4096, 생성할 텍스트의 최대 토큰 수
#     chunk_overlap: int = 0 # 텍스트를 여러 청크로 나눌 때 청크 간에 중첩되는 토큰 수
#     chunk_size: int = 512 # 텍스트를 나눌 때 각 청크의 최대 토큰 수를 지정
#     embed_model: str =  # 임베딩 모델의 이름
#     reader # 문서 읽기 방법
#     splitter # 텍스트 분할 방법