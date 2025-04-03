import json
from typing import Dict

from src.service.interface.arb_supporter.llm import LLM
from src.utils.constants import Prompt
from src.service.interface.arb_supporter.confirmation_agent import ConfirmationAgent

class ConfirmationAgentImpl(ConfirmationAgent):
    
    def __init__(
        self, 
        llm: LLM
    ) -> None:
        super(ConfirmationAgentImpl, self).__init__()
        self.llm = llm


    @staticmethod
    def __confirm_user_intent(query: str) -> str:
        user_prompt = f"""
        
        The user's query usually contains words such "confirm", "accept", "OK", "Let's do it", "I'm ready", so on. These words' pattern is the confirmation of user's query
        
        # ***User's query***
        {query}

        # ***Example Scenarios:***
        
        - ***User***: "It's enough"
        - ***Assistant***: {{"is_confirmed": 0}}
        
        - ***User***: "I want to confirm it"
        - ***Assistant***: {{"is_confirmed": 1}}
        
        - ***User***: "Yes, delete it."
        - ***Assistant***: {{"is_confirmed": 1}}

        - ***User***: "No, I changed my mind."
        - ***Assistant***: {{"is_confirmed": 0}}

        - ***User***: "Yes, that's correct."
        - ***Assistant***: {{"is_confirmed": 1}}

        - ***User***: "No, I meant for the last week."
        - ***Assistant***: {{"is_confirmed": 0}}
        """
        return user_prompt


    def get_decision(
        self,
        query: str
    ) -> Dict[str, str]:
        system_prompt = Prompt.LLM_CONFIRMATION_SYSTEM_PROMPT

        user_prompt = self.__confirm_user_intent(query)

        format_schema = {
            "type": "object",
            "properties": {
                "is_confirmed": {
                    "type": "integer"
                }
            },
            "required": [
                "is_confirmed"
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

        return json.loads(response)['is_confirmed']
