import os 

from src.service.interface.arb_service.arb_service import ARBService
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
from src.service.interface.arb_supporter.function_calling_conversation_agent import FunctionCallingConversationAgent
from src.model.Alpha_metadata import AlphaMetadata

class ARBServiceImpl(ARBService):
    def __init__(self, 
                 normal_conversation_agent: NormalConversationAgent,
                 function_calling_conversation_agent: FunctionCallingConversationAgent):
        self.normal_conversation_agent = normal_conversation_agent
        self.function_calling_conversation_agent = function_calling_conversation_agent


    def get_responding(self, user_id: str, message: str) -> str:
        response = self.function_calling_conversation_agent.responding(user_id, message)
        print("😊 ME: ", message)
        print("🤖 BOT: ", response)
        return response
    

    def get_alpha_response(self, user_id: str, message: str) -> AlphaMetadata:
        meta_data_response = self.function_calling_conversation_agent.alpha_responding(user_id, message)
        print("😊 ME: ", message)
        print("🤖 BOT: ", meta_data_response.response)
        return meta_data_response
