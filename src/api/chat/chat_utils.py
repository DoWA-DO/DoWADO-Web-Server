# """
# 진로 상담 챗봇 API - 채팅 메시지 생성
# """
# import redis
# from typing import Dict, List, Optional
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
# from src.settings.index import ChatOptions


# def generation(chat_opts: ChatOptions, document) -> Dict:
#     ...


# class ChatGenerator:
#     def __init__(self):
#         self.SIMILARITY_THRESHOLD = config["similarity_k"]
#         self.llm = ChatOpenAI(
#             model       = config['llm_predictor']['model_name'],
#             temperature = config['llm_predictor']['temperature']
#         )
#         self.vector_store   = self.init_vector_store()
#         self.retriever  = self.init_retriever()
#         self.chain      = self.init_chain()
#         self.session_histories = {}    
#         self.redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])
        
    
#     def init_vector_store():
#         """ Vector store 초기화 """
#         embeddings = OpenAIEmbeddings( model=config['embed_model']['model_name'] )
#         vector_store = Chroma(
#             persist_directory=config["chroma"]["persist_dir"], 
#             embedding_function=embeddings
#         )
#         print(f"[초기화] vector_store 초기화 완료")
#         return vector_store
        
#     def init_retriever():
#         """ Retriever 초기화 
#         다른 검색방법 사용해보기
#         Hybrid Search
#         """
#         retriever = self.vector_store.as_retriever(
#             search_kwargs = {"k": config["retriever_k"]},
#             search_type   = "similarity"
#         )
#         print(f"[초기화] retriever 초기화 완료")
#         return retriever
        
#     def init_chain():
#         """ chain 초기화 
#         리트리버 전용 체인으로 변경해보기
#         create_stuff_documents_chain[현재 사용] : 문서 목록을 가져와서 모두 프롬프트로 포맷한 다음 해당 프롬프트를 LLM에 전달합니다.
#         create_history_aware_retriever : 대화 기록을 가져온 다음 이를 사용하여 검색 쿼리를 생성하고 이를 기본 리트리버에 전달
#         create_retrieval_chain : 사용자 문의를 받아 리트리버로 전달하여 관련 문서를 가져옵니다. 그런 다음 해당 문서(및 원본 입력)는 LLM으로 전달되어 응답을 생성
#         """
        
#         # 사용자의 질문 문맥화 <- 프롬프트 엔지니어링
#         history_aware_retriever = create_history_aware_retriever(
#             self.llm, self.retriever, contextualize_q_prompt
#         )
        
#         # 응답 생성 + 프롬프트 엔지니어링
#         question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
#         # 최종 체인 생성
#         rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

#         print("[초기화] RAG chain 초기화 완료")
#         return rag_chain
    
#     def chat_generator(self, question: str, session_id: str) -> dict:
#         # 채팅 기록 관리
#         def get_session_history(session_id: str) -> BaseChatMessageHistory:
#             if session_id not in self.session_histories:
#                 self.session_histories[session_id] = ChatMessageHistory()
#                 print(f"[히스토리 생성] 새로운 히스토리를 생성합니다. 세션 ID: {session_id}")
#             return self.session_histories[session_id]

#         conversational_rag_chain = RunnableWithMessageHistory(
#             self.chain,
#             get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )

#         response = conversational_rag_chain.invoke(
#             {"input": question},
#             config={"configurable": {"session_id": session_id}}
#         )

#         print(f'[응답 생성] 실제 모델 응답: response => \n{response}\n')
#         print(f"[응답 생성] 세션 ID [{session_id}]에서 답변을 생성했습니다.")

#         # Redis에 대화 기록 저장
#         chat_history_key = f"chat_history:{session_id}"
#         try:
#             print(f'--------> Redis 키: {chat_history_key}')
#             chat_history = self.redis_client.get(chat_history_key)
#             print('-------->',chat_history)
#             if chat_history:
#                 chat_history = json.loads(chat_history)
#             else:
#                 chat_history = []

#             chat_history.append({"question": question, "answer": response["answer"]})
#             print(f'=========> 저장할 대화 기록: {chat_history}')
#             print(f'=========> 저장할 대화 기록 json: {json.dumps(chat_history)}')
#             self.redis_client.set(chat_history_key, json.dumps(chat_history))        
#             print(f"[Redis 저장] 세션 ID [{session_id}]의 대화 기록을 Redis에 저장했습니다.")
#         except Exception as e:
#             print(f"[Redis 저장 실패] 세션 ID [{session_id}]의 대화 기록 저장 중 오류 발생: {e}")

#         return response["answer"]