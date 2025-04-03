import json
from typing import List
from src.service.interface.arb_supporter.task_detection_agent import TaskDetectionAgent
from src.service.interface.arb_supporter.llm import LLM

class TaskDetectionAgentImpl(TaskDetectionAgent):
    """
    Implementation of the TaskDetection abstract base class.
    """

    def __init__(
        self,
        llm: LLM
    ) -> None:
        super(TaskDetectionAgentImpl, self).__init__()
        
        self.llm = llm
    
    
    @staticmethod
    def __detect_task_intent(query: str) -> str:
        user_prompt = f"""
        # ***User's query***
        {query}

        # **Key Guidelines:**
        - Match the user's query to one of the predefined task types listed below.
        - If the query does not match any task type, respond with "Task type not recognized."
        - Provide a concise summary of the detected task type for confirmation.
        - Respond in a polite and professional tone, maintaining a focus on accuracy and helpfulness.

        # ***Predefined Task Types:***
        - Winlost Report
        - Turnover Report
        - Bet Count Report
        - Net Turnover Report
        - Gross Commission
        - Member Report
        - Agent Report
        - Master Report
        - Super Report
        - Company Report
        - Reward (USD) Report
        - Customer / Username Report
        - Outstanding Report
        - Statement Report
        - Create a new customer information (account/member/agent/master/super)
        - Bet List Management
        - Bet Forecasting
        - Transfers
        - Risk Management

        # ***Example Scenarios:***
        - ***User***: "I want to get winlost and turnover report."
        - ***Assistant***: ["Winlost Report", "Turnover Report"]

        - ***User***: "Generate a member and agent report."
        - ***Assistant***: ["Member Report", "Agent Report"]

        - ***User***: "I need a statement and risk management report."
        - ***Assistant***: ["Statement Report", "Risk Management"]
        """
        return user_prompt

    def detect_task(self, query: str) -> List[str]:
        """
        Detect the task from the given query.

        Args:
            query (str): The input query from the user.

        Returns:
            List[str]: A list of detected task types.
        """

        system_prompt = """
        You are a task detection agent responsible for identifying and categorizing the type of task requested by the user. Your primary goal is to determine whether the user's query matches one of the predefined task types and confirm the detected task type explicitly.
        """
        user_prompt = self.__detect_task_intent(query)

        format_schema = {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "tasks"
            ]
        }

        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.send_request(
            message=message,
            format_schema=format_schema,
            endpoint='/api/chat'
        )

        response = json.loads(response['message']['content'])

        # Call the task detection agent to process the query
        detected_tasks = response['tasks']
        
        return detected_tasks