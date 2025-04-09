import json
from typing import Dict, Any

from src.service.interface.arb_supporter.function_calling_agent import FunctionCallingAgent
from src.service.interface.arb_supporter.llm import LLM

class FunctionCallingExtraction(FunctionCallingAgent):
    def __init__(
        self,
        llm: LLM
    ) -> None:
        super(FunctionCallingExtraction, self).__init__()
        
        self.llm = llm
        self.format_output = {
        "type": "object",
        "properties": {
            "function_called": {
                "type": "string",
                "description": "The name of the function to call",
                "enum": [
                    '/get_winlost_report',
                    # '/get_betcount_report',
                    '/get_turnover_report',
                    # '/get_net_turnover_report',
                    # '/get_gross_comm_report',
                    # '/get_member_report',
                    # '/get_agent_report',
                    # '/get_master_report',
                    # '/get_super_report',
                    # '/get_company_report',
                    # '/get_reward_report',
                    'N/A'
                ]
            }
        },
        "required": ["function_called"]
    }
        self.system_prompt = """
        You are an AI assistant that helps determine which function to call based on user input.
        Available functions:
            - /get_winlost_report: Get Win/Loss reports with filtering by date, product, and user level. Supports exporting reports (CSV/PDF), comparing trends across time periods, highlighting biggest winners/losers, and detecting unusual betting patterns.
            - /get_turnover_report: Get turnover/revenue reports showing total betting volume/activity, with breakdowns by product, date range and user level. Includes trend analysis and comparison features.

        Determine which function best matches the user's request and return it in JSON format like:
        {
            "function_called": "/function_name"
        }
        """



    def __get_user_prompt(self, query: str) -> str:
        prompt = """
            User request: {query}

            # ⚠️Note that:
            - If the user request is not related to the function, return "N/A"
            - If the user request is not clear, return "N/A"
            - If the user request is not related to the function, return "N/A"
            - If the user request does not contain any functions or report words, return "N/A"
            
            
            #📝Example requests and responses:
            
            Input: "I need to see the win/loss report from last week"
            Output: {{
                "function_called": "/get_winlost_report"
            }}

            Input: "I want to get the reward report"
            Output: {{
                "function_called": "/get_reward_report"
            }}

            Input: "I want to take bet count report for user 123"
            Output: {{
                "function_called": "/get_betcount_report"
            }}

            Input: "Get me the get gross commission report for March transactions"
            Output: {{
                "function_called": "/get_gross_comm_report"
            }}

            Input: "I want get performance of abc1 last week"
            Output: {{
                "function_called": "N/A"
            }}
            
            Input: "Hello how are you today?"
            Output: {{
                "function_called": "N/A"
            }}
            
            Input: "I want Sportsbook only"
            Output: {{
                "function_called": "N/A"
            }}
            
            Input: "I want change to a little bit, I want to get Product Virtual Sports and product detail Saba Basketball with user level Super Agent"
            Output: {{
                "function_called": "N/A"
            }}
            
            Based on this request, which function should be called? Return only the JSON response.
        """.format(query=query)
        
        return prompt



    def __process_function_calling(self, query: str) -> str:
    
        # Construct the prompt for function determination with examples
        user_prompt = self.__get_user_prompt(query)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages, 
            format_schema=self.format_output
        )
        
        if 'function_called' in json.loads(response):
            return json.loads(response)['function_called']
        else:
            return 'N/A'



    def call_function(self, message: str) -> Dict[str, Any]:
        # Process the message and get the function to call
        function_result = self.__process_function_calling(message)
        
        return function_result