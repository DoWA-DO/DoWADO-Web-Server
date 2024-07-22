# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import datetime
# from src.api.v1.chat import chat_service

# from src.api.v1.chat.chatbot_dto import ChatCreateResponse
# from src.api.v1.login.login_control import get_current_user
# from src.database.model import ChatLog

# async def create_chatbot_message(
#     query: str,
#     db: AsyncSession,
#     current_user: dict = Depends(get_current_user)
# ):
#     response = await chat_service.get_chatbot_message(query)
#     chat_message = ChatLog(
#         chat_student_email = current_user,
#         chat_content=query,
#         chat_response=response,
#         chat_date=datetime.now(),
#     )
#     db.add(chat_message)
#     await db.commit()
#      # Create a response object
#     chat_response = ChatCreateResponse(
#         id=chat_message.id,  # Assuming ChatLog has an 'id' attribute
#         chat_student_email=chat_message.username,  # Replace with the actual student's email if available
#         chat_content=query,
#         chat_response=response,
#         chat_date=chat_message.chat_date,
#         chat_status=0  # Replace with the actual status if available
#     )
#     return chat_response

