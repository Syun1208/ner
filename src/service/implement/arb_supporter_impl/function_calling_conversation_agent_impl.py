import os
import json
import requests
from typing import List

from src.service.interface.arb_supporter.function_calling_conversation_agent import FunctionCallingConversationAgent
from src.utils.utils import load_json, to_json
from src.utils.functions import *
from src.utils.constants import Prompt as p
from src.model.Alpha_metadata import AlphaMetadata

class FunctionCallingConversationAgentImpl(FunctionCallingConversationAgent):
    def __init__(self, history_context_folder: str, function_calling_conversation_agent_config:dict):
        self.history_context_folder = history_context_folder
        self.function_calling_conversation_agent_config = function_calling_conversation_agent_config
        
        if not os.path.exists(self.history_context_folder):
            os.makedirs(self.history_context_folder)

        self.__load_function_list()

    
    def __get_history_conversation_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + ".json")
    
    def __get_nearest_function_arguments_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + "_function_arguments.json")
    
    def __load_function_list(self):
        function_list_path = self.function_calling_conversation_agent_config['function_list_path']
        self.function_list =  load_json(function_list_path)
    def __get_function_by_name(self, function_name: str) -> dict:
        for function in self.function_list:       
            if function['function']['name'] == function_name:
                return function 
    
    def start_conversation(self, user_id: int) -> List[dict]:
        history_context_path = self.__get_history_conversation_path(user_id)
        if os.path.exists(history_context_path):
            return load_json(history_context_path)
        else:
            return [{"role": "user", "content": p.FUNCTION_CALLING_SYSTEM_PROMT}] 

    def responding(self, user_id: int, message: str) -> str:
        conversation_chain = self.start_conversation(user_id)
        conversation_chain.append({"role": "user", "content": message})

        # Call Ollama API
        headers = {
            "Content-Type": "application/json"
        }
        model = 'qwen2.5:14b'
        data = {
            "model": model,
            "messages": conversation_chain,
            "tools": self.function_list,
            "stream": False
        }
        api_url = 'https://ollama.selab.edu.vn/api/chat'
        response = requests.post(api_url, headers=headers, data=json.dumps(data), auth = ('hvtham', 'assembler'))
        response = response.json()

        #print("RESPONSE: ", response)
        if 'tool_calls' in response['message'].keys():
            print("🌐 TOOL CALLS: ", response['message']['tool_calls'][0])
            reply = "Request completed! Can I assist you with anything else?"
        else: 
            # Get the response content
            reply = response['message']['content']

        conversation_chain.append({"role": "assistant", "content": reply })
        to_json(conversation_chain, self.__get_history_conversation_path(user_id))
        return reply
    
    def alpha_responding(self, user_id: int, message: str) -> AlphaMetadata:
        conversation_chain = self.start_conversation(user_id)
        conversation_chain.append({"role": "user", "content": message})

        # initial 
        is_action = False
        endpoint = None
        params = None
        # Call Ollama API
        headers = {
            "Content-Type": "application/json"
        }
        model = 'qwen2.5:14b'
        data = {
            "model": model,
            "messages": conversation_chain,
            "tools": self.function_list,
            "stream": False
        }
        api_url = 'https://saillm.oneops.net/api/chat'
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response = response.json()

        #print("RESPONSE: ", response)
        if 'tool_calls' in response['message'].keys():
            print("🌐 TOOL CALLS: ", response['message']['tool_calls'][0])
            reply = None
            is_action = True
            endpoint = response['message']['tool_calls'][0]['function']['name']
            params = response['message']['tool_calls'][0]['function']['arguments']
        else: 
            # Get the response content
            reply = response['message']['content']

        conversation_chain.append({"role": "assistant", "content": reply })
        to_json(conversation_chain, self.__get_history_conversation_path(user_id))

        return AlphaMetadata(user_id = user_id, 
                             is_new_session = False, 
                             is_action = is_action, 
                             endpoint = endpoint, 
                             params = params, 
                             response = reply)
    
    
