import os
import json
import requests
from typing import List

from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
from src.utils.utils import load_json, to_json

class NormalConversationAgentImpl(NormalConversationAgent):
    def __init__(self, history_context_folder: str, normal_conversation_agent_config:dict):
        self.history_context_folder = history_context_folder
        self.normal_conversation_agent_config = normal_conversation_agent_config
        if not os.path.exists(self.history_context_folder):
            os.makedirs(self.history_context_folder)

    
    def __get_history_conversation_path(self, user_id: int, session_id: str):
        return os.path.join(self.history_context_folder, str(user_id) + "_" + session_id + ".json")
    
    
        
    def start_conversation(self, user_id: int, session_id: str) -> List[dict]:
        history_context_path = self.__get_history_conversation_path(user_id, session_id)
        if os.path.exists(history_context_path):
            return load_json(history_context_path)
        else:
            return [] 

    def responding(self, user_id: int, session_id: str, message: str) -> str:
        conversation_chain = self.start_conversation(user_id, session_id)
        conversation_chain.append({"role": "user", "content": message})

        # Call Ollama API
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self.normal_conversation_agent_config['model'],
            "messages": conversation_chain,
            "stream": False
        }
        response = requests.post(self.normal_conversation_agent_config['llm_api_url'], headers=headers, data=json.dumps(data))
        response = response.json()

        # Get the response content
        reply = response['message']['content']

        # Update history
        conversation_chain.append({"role": "assistant", "content": reply})
        to_json(conversation_chain, self.__get_history_conversation_path(user_id, session_id))
        return reply
    
    
