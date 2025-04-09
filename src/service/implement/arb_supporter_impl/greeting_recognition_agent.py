import json
from typing import Dict

from src.service.interface.arb_supporter.llm import LLM
from src.utils.constants import Prompt
from src.service.interface.arb_supporter.confirmation_agent import ConfirmationAgent

class GreetingRecognitionAgentImpl(ConfirmationAgent):
    
    def __init__(
        self, 
        llm: LLM
    ) -> None:
        super(GreetingRecognitionAgentImpl, self).__init__()
        self.llm = llm


    @staticmethod
    def __greeting_checker_user_intent(query: str) -> str:
        user_prompt = f"""

        # ***User's query***
        {query}
        
        # General conversation guidelines:
        - Your task is to check if the user's query is a greeting conversation or not.
        - The user's query must be greeting conversation when the user's query is not related to any report question.
        - If the user's query is a greeting conversation, return 1.
        - If the user's query is not a greeting conversation, return 0.
        - The response should be in JSON format.
        

        # ***Example Scenarios:***
        
        - ***User***: "Hello bot how are you today ?"
        - ***Assistant***: {{"is_normal_conversation": 1}}
        
        - ***User***: "See you later. Bye."
        - ***Assistant***: {{"is_normal_conversation": 1}}

        - ***User***: "I want change to a little bit, I want to get Product Virtual Sports and product detail Saba Basketball with user level Super Agent"
        - ***Assistant***: {{"is_normal_conversation": 0}}

        - ***User***: "I want to get Winlost Report"
        - ***Assistant***: {{"is_normal_conversation": 0}}

        - ***User***: "Hey what is the weather in Tokyo?"
        - ***Assistant***: {{"is_normal_conversation": 1}}
        """
        return user_prompt


    def get_decision(
        self,
        query: str
    ) -> Dict[str, str]:
        system_prompt = """
        You are a helpful assistant that can check if the user's query is a greeting conversation or not.
        
        # General conversation guidelines:
        - The user's query must be greeting conversation when the user's query is not related to any report question.
        - If the user's query is a greeting conversation, return 1.
        - If the user's query is not a greeting conversation, return 0.
        - The response should be in JSON format.
        """

        user_prompt = self.__greeting_checker_user_intent(query)

        format_schema = {
            "type": "object",
            "properties": {
                "is_normal_conversation": {
                    "type": "integer"
                }
            },
            "required": [
                "is_normal_conversation"
            ]
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages,
            format_schema=format_schema
        )

        if 'is_normal_conversation' in json.loads(response):
            return json.loads(response)['is_normal_conversation']
        else:
            return 0
