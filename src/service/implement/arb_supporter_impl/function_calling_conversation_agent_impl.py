import os
import gc
from datetime import datetime
from typing import List, Dict
from langdetect import detect

from src.service.interface.arb_supporter.function_calling_conversation_agent import FunctionCallingConversationAgent
from src.utils.utils import load_json, to_json
from src.utils.constants import Prompt as p
from src.model.alpha_metadata import AlphaMetadata
from src.service.interface.arb_supporter.llm import LLM
from src.service.interface.arb_supporter.confirmation_agent import ConfirmationAgent
from src.service.interface.arb_supporter.task_detection_agent import TaskDetectionAgent


class FunctionCallingConversationAgentImpl(FunctionCallingConversationAgent):
    def __init__(
        self, 
        llm: LLM,
        confirmation_agent: ConfirmationAgent,
        task_detection_agent: TaskDetectionAgent,
        history_context_folder: str, 
        function_calling_conversation_agent_config: Dict[str, str]
    ) -> None:
        super(FunctionCallingConversationAgentImpl, self).__init__()
        
        self.llm = llm
        self.confirmation_agent = confirmation_agent
        self.task_detection_agent = task_detection_agent
        self.history_context_folder = history_context_folder
        self.function_calling_conversation_agent_config = function_calling_conversation_agent_config
        
        if not os.path.exists(self.history_context_folder):
            os.makedirs(self.history_context_folder)

        self.__load_function_list()
    
    
    
    def __get_current_tasks_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + "_current_tasks.json")
    
    
    
    def __get_history_conversation_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + ".json")
    
    
    
    def __get_nearest_function_path(self, user_id: int):
        return os.path.join(self.history_context_folder, str(user_id) + "_nearest_function.json")
    
    
    
    def __load_function_list(self):
        function_list_path = self.function_calling_conversation_agent_config['function_list_path']
        if os.path.exists(function_list_path):
            self.function_list = []
            for file_name in os.listdir(function_list_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(function_list_path, file_name)
                    self.function_list.extend(load_json(file_path))



    def start_conversation(self, user_id: int) -> List[dict]:
        history_context_path = self.__get_history_conversation_path(user_id)
        nearest_context_path = self.__get_nearest_function_path(user_id)
        current_tasks_path = self.__get_current_tasks_path(user_id)
        
        if os.path.exists(history_context_path):
            self.conversation_chain = load_json(history_context_path)
            self.nearest_function = load_json(nearest_context_path)
            self.current_tasks = load_json(current_tasks_path)
            
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.conversation_chain = [
                {
                    "role": "system", 
                    "content": f"Now is {now}" + p.FUNCTION_CALLING_SYSTEM_PROMT,
                    "defined_tasks": []
                }
            ] 
            self.nearest_function = {
                'nearest_function': ""
            }
            self.current_tasks = {
                'defined_tasks': []
            }
    
    
    
    def get_response(
        self, 
        user_id: int, 
        message: str
    ) -> AlphaMetadata:
        
        self.start_conversation(user_id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Detect type of language
        detected_language = detect(message)
        
        # Check length of conversation and get top 10 latest conversation
        if len(self.conversation_chain) >= 10:
            self.conversation_chain = self.conversation_chain[-10:]
        
        # Define tasks from query
        defined_tasks = self.task_detection_agent.detect_task(message)
        
        # Save all defined tasks and historical conversations
        self.conversation_chain.append({
            "role": "user", 
            "content": message + f"(MUST confirm for me all agurments and actions before calling tool! Now is {now})! Please response me by {detected_language}"
        })

        # Initialize flags
        is_action = False
        endpoint = None
        params = None
        is_new_session = False
        
        # Call Ollama API
        response = self.llm.invoke(
            messages=self.conversation_chain,
            tools=self.function_list
        )
        print(response)
        # NOTE: Handle Logic of Scenarios
        # Case 1: is_new_session (there is any change in current tasks)
        print("current_tasks: ", self.current_tasks['defined_tasks'])
        if len(self.current_tasks['defined_tasks']) == 0:
            print(f"Update current_tasks from {self.current_tasks['defined_tasks']} to {defined_tasks}")
            self.current_tasks['defined_tasks'] = defined_tasks
    
        if defined_tasks != self.current_tasks['defined_tasks']:
            self.current_tasks['defined_tasks'] = defined_tasks
            is_new_session = True
        
        # Case 2: is_action
        is_confirmed = self.confirmation_agent.get_decision(query=message)
        print("is_confirmed: ", is_confirmed)
        if is_confirmed and 'tool_calls' in response['message'].keys():
            reply = None
            is_action = True
            endpoint = response['message']['tool_calls'][0]['function']['name']
            params = response['message']['tool_calls'][0]['function']['arguments']
            
            self.conversation_chain.append({
                "role": "tool", 
                "tool_calls": response['message']['tool_calls']
            })
            
            # Update function 
            if len(self.nearest_function.keys()) == 0:
                self.nearest_function['nearest_function'] = endpoint
            
            if self.nearest_function['nearest_function'] != endpoint:
                self.nearest_function['nearest_function'] = endpoint
        
        else:
            # Get the response content
            reply = response['message']['content']
            self.conversation_chain.append({"role": "assistant", "content": reply })

        # Save the useful information into json
        to_json(self.conversation_chain, self.__get_history_conversation_path(user_id))
        to_json(self.nearest_function, self.__get_nearest_function_path(user_id))
        to_json(self.current_tasks, self.__get_current_tasks_path(user_id))
        
        del self.conversation_chain, self.nearest_function
        gc.collect()

        return AlphaMetadata(
            user_id=user_id, 
            is_new_session=is_new_session, 
            is_action=is_action, 
            endpoint=endpoint, 
            params=params, 
            response=reply
        )
    
    
