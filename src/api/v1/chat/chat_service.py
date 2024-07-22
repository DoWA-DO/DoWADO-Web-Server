# # service.py
# from datetime import datetime

# class ChatService:
#     def __init__(self, chatbot):
#         self.chatbot = chatbot

#     async def get_chatbot_message(self, query: str) -> str:
#         """
#         Communicates with the chatbot to get a response for the given query.
        
#         Args:
#             query (str): The user's chat message.
            
#         Returns:
#             str: The chatbot's response.
#         """
#         # Here you would normally have the logic to get the response from the chatbot.
#         # For the sake of example, let's assume it's a simple echo response.
#         response = await self.chatbot.get_response(query)
#         return response

# # Assuming you have a chatbot instance that the service uses.
# class Chatbot:
#     async def get_response(self, query: str) -> str:
#         # Placeholder for chatbot interaction logic
#         return f"Chatbot response to: {query}"

# # Create an instance of the ChatService with a dummy Chatbot instance
# chat_service = ChatService(Chatbot())


