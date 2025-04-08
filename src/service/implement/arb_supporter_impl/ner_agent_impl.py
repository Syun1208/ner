import json
from typing import List, Dict, Any

from src.service.interface.arb_supporter.ner_agent import NerAgent
from src.utils.constants import AlphaWinlostInfo as a
from src.service.interface.arb_supporter.llm import LLM
from src.utils.utils import get_current_datetime, get_current_year, get_current_month

class NerAgentImpl(NerAgent):
    """
    Implementation of NerAgent using Ollama API for Named Entity Recognition.
    """
    
    def __init__(
        self,
        llm: LLM
    ) -> None:
        """
        Initialize the NerAgentImpl with Ollama API configuration.
        
        Args:
            url (str): The Ollama API endpoint URL
            model (str): The model name to use for NER
        """
        self.llm = llm
        self.system_prompt = "You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail"
        self.format = {
            "type": "object",
            "properties": {
                "date_range": {"type": "string"},
                "from_date": {"type": "string"},
                "to_date": {"type": "string"},
                "product": {"type": "string"},
                "product_detail": {"type": "string"},
                "level": {"type": "string"},
                "user": {"type": "string"}
            },
            "required": ["date_range", "from_date", "to_date", "product", "product_detail", "level", "user"]
        }



    def _get_user_prompt(self, text: str) -> str:
        current_date = get_current_datetime()
        current_year = get_current_year()
        current_month = get_current_month()

        user_prompt = f"""
        Current date: {current_date}
        Current year: {current_year}
        Current month: {current_month}

        Extract the most relevant keywords from the following sentence: '{text}'. 
        Focus on important nouns that convey the core meaning. 
        Detect any words related to dates such as tomorrow, today, last week, next year, so on, following the example below.
        Help me convert the date range to the format of YYYY-MM-DD to YYYY-MM-DD.
        For date range, please help me convert it to from_date and to_date in DD/MM/YYYY format following these rules:

        1. If a single date is mentioned (e.g. "day 10"):
           - Use current month and year {current_year} and {current_month}
           - Set both from_date and to_date to that date
           Example: "day 10" in March 2025 -> from_date: 10/03/2025, to_date: 10/03/2025

        2. If a date range is specified (e.g. "01/02/2024 to 15/02/2024"):
           - Keep the dates as specified in DD/MM/YYYY format
           Example: "01/02/2024 to 15/02/2024" -> from_date: 01/02/2024, to_date: 15/02/2024

        3. If relative dates are mentioned:
           - "today" -> Use {current_date} for both
           - "yesterday" -> Use yesterday's date for both from current date {current_date}
           - "last week" -> from_date is 7 days ago, to_date is today from current date {current_date}
           - "last month" -> from_date is 1st of previous month, to_date is last day of previous month from current date {current_date}
           - "last year" -> from_date is Jan 1st of previous year, to_date is Dec 31st of previous year from current date {current_date}
           - "this week" -> from_date is Monday of current week, to_date is today from current date {current_date}
           - "this month" -> from_date is 1st of current month, to_date is today from current date {current_date}
           - "this year" -> from_date is Jan 1st of current year, to_date is today from current date {current_date}
           
        4. If a month range is specified (e.g. "1/1 to 31/1"):
           - Use current year {current_year}
           - Set from_date to first day of specified month 
           - Set to_date to last day of specified month
           Example: "1/1 to 31/1" in {current_year} -> from_date: 01/01/{current_year}, to_date: 31/01/{current_year}
           
        5. If no date is specified:
           - Set date_range as "N/A"
           - Set both from_date and to_date as "N/A"
           
        If no relevant keywords are detected, return 'All' (except for dates, you must fill 'N/A').
        If the date range is not specified, please return 'N/A' for date_range.
        If the product is not specified, please return 'All' for product.
        If the product detail is not specified, please return 'All' for product_detail.
        If the level is not specified, please return 'All' for level.
        If the user is not specified, please return 'N/A' for user.
        
        Here is the list of product and product detail you should detect:
        ### PRODUCT = {a.PRODUCT}
        ### PRODUCT_DETAIL = {a.PRODUCT_DETAIL}
        ### LEVEL = {a.LEVEL}
        
        Occasionaly, "user" keyword may appear some words such as "master*", "super*", "admin*", "user*", "agent*" where * is any characters.
        
        Example 1:
        ## User: Get me a Win Loss Detail Report on day 10
        ## Output:
        {{
            "date_range": "day 10",
            "from_date": "10/03/2025",
            "to_date": "10/03/2025",
            "product": "All",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        
        Example 2:
        ## User: Get me a Win Loss Detail Report for Direct Member who played Product Detail Sportsbook in Sportsbook Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "product": "Sportsbook",
            "product_detail": "Sportsbook",
            "level": "Direct Member",
            "user": "N/A"
        }}
        
        Example 3:
        ## User: Get me a Win Loss Detail Report for Super Agent who played Product Detail SABA Basketball in SABA Basketball Product from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024",
            "product": "SABA Basketball",
            "product_detail": "SABA Basketball",
            "level": "Super Agent",
            "user": "N/A"
        }}
        
        Example 4:
        ## User: Win/Loss details for Product Sportsbook
        ## Output:
        {{
            "date_range": "N/A",
            "from_date": "N/A",
            "to_date": "N/A",
            "product": "Sportsbook",
            "product_detail": "All",
            "level": "All",
            "user": "N/A"
        }}
        """
        return user_prompt



    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Process the input text and extract named entities using Ollama API.
        
        Args:
            text (str): The input text to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted entities and their metadata
        """
        user_prompt = self._get_user_prompt(text)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.invoke(
            messages=messages,
            format_schema=self.format,
            endpoint='/api/chat'
        )
        
        if not json.loads(response):
            return {
                "date_range": "N/A",
                "from_date": "N/A",
                "to_date": "N/A",
                "product": "All",
                "product_detail": "All",
                "level": "All",
                "user": "N/A"
            }
            
        return json.loads(response)



    def get_entity_types(self) -> List[str]:
        """
        Get the list of entity types that this NER agent can recognize.
        
        Returns:
            List[str]: List of supported entity types
        """
        return ["date_range", "from_date", "to_date", "product", "product_detail", "level", "user"]