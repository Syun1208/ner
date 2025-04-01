import os
import gc
import json
import requests
from datetime import datetime
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
    
    def __get_nearest_function_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + "_nearest_function.json")
    
    def __load_function_list(self):
        function_list_path = self.function_calling_conversation_agent_config['function_list_path']
        self.function_list =  load_json(function_list_path)
    
    def start_conversation(self, user_id: int) -> List[dict]:
        history_context_path = self.__get_history_conversation_path(user_id)
        nearest_context_path = self.__get_nearest_function_path(user_id)
        if os.path.exists(history_context_path):
            self.conversation_chain = load_json(history_context_path)
            self.nearest_function = load_json(nearest_context_path)
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conversation_chain = [{"role": "system", "content": f"Now is {now}" + p.FUNCTION_CALLING_SYSTEM_PROMT}] 
            self.nearest_function = {}
    
    def get_response(self, user_id: int, message: str) -> AlphaMetadata:
        self.start_conversation(user_id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_chain.append({"role": "user", "content": message + f"(MUST confirm for me all agurments and actions before calling tool! Now is {now})"})

        # initial 
        is_action = False
        endpoint = None
        params = None
        is_new_session = False
        # Call Ollama API
        headers = {
            "Content-Type": "application/json"
        }
        model = 'qwen2.5:14b'
        data = {
            "model": model,
            "messages": self.conversation_chain,
            "tools": self.function_list,
            "stream": False
        }
        api_url = 'https://ollama.selab.edu.vn/api/chat'
        response = requests.post(api_url, headers=headers, data=json.dumps(data), auth = ('hvtham', 'assembler'))
        response = response.json()

        #print("RESPONSE: ", response)
        if 'tool_calls' in response['message'].keys():
            reply = None
            is_action = True
            endpoint = response['message']['tool_calls'][0]['function']['name']
            params = response['message']['tool_calls'][0]['function']['arguments']
            self.conversation_chain.append({"role": "tool", "tool_calls": response['message']['tool_calls']})

            if len(self.nearest_function.keys()) == 0:
                self.nearest_function['nearest_function'] = endpoint
            else:
                if self.nearest_function['nearest_function'] != endpoint:
                    self.nearest_function['nearest_function'] = endpoint
                    is_new_session = True
        else: 
            # Get the response content
            reply = response['message']['content']
            self.conversation_chain.append({"role": "assistant", "content": reply })

        
        to_json(self.conversation_chain, self.__get_history_conversation_path(user_id))
        to_json(self.nearest_function, self.__get_nearest_function_path(user_id))
        del self.conversation_chain, self.nearest_function
        gc.collect()

        return AlphaMetadata(user_id = user_id, 
                             is_new_session = is_new_session, 
                             is_action = is_action, 
                             endpoint = endpoint, 
                             params = params, 
                             response = reply)
    
    
