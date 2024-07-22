"""
프롬프트 초기화
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 사용자 질문 맥락화 프롬프트
contextualize_q_system_prompt = """
당신의 주요 목표는 사용자의 질문을 이해하기 쉽게 다시 작성하는 것입니다.
사용자의 질문과 채팅 기록이 주어졌을 때, 채팅 기록의 맥락을 참조하세요.
채팅 기록이 없더라도 이해할 수 있는 독립적인 질문으로 작성하세요.
질문에 바로 대답하지 말고, 필요하다면 질문을 다시 작성하세요. 그렇지 않다면 질문을 그대로 반환합니다.        
"""
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


# 질문 프롬프트
qa_system_prompt = """
당신의 역할은 학생들을 위한 진로 상담사입니다. 
학생들이 진로,직업 관련 정보에 대해서 물어보면 아래에 주어지는 검색된 내용을 토대로 질문에 대해 답변하세요.
검색된 정보를 활용하여 사실인 정보만을 대답해야합니다. 
답을 모를 경우, '죄송합니다. 제가 아직 모르는 내용입니다.' 라고 대답하세요. 
최대한 명확하고 이해하기 쉽게 대답하세요.

{context}
"""
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])