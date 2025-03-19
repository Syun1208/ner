import os 

from src.service.interface.arb_service.arb_service import ARBService
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
class ARBServiceImpl(ARBService):
    def __init__(self, normal_conversation_agent: NormalConversationAgent):
        self.normal_conversation_agent = normal_conversation_agent


    def get_responding(self, user_id: str, session_id: str, message: str) -> str:
        response = self.normal_conversation_agent.responding(user_id, session_id, message)
        print("😊 ME: ", message)
        print("🤖 BOT: ", response['text'])
        return response

    
