from typing import Dict, Any

from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
from src.service.interface.arb_supporter.llm import LLM
from src.utils.constants import FUNCTION_MAPPING_NAME

class CasualConversationAgentImpl(NormalConversationAgent):
    
    def __init__(
        self, 
        llm: LLM
    ) -> None:
        self.llm = llm
        self.system_prompt = """
            You are a friendly and helpful S.A.I's Assistant trained to handle conversations about Win/Loss reports and other queries in a casual yet professional manner.

            Your main responsibilities are:
            1. Help users get the information they need about Win/Loss reports 📖
            2. Guide users to provide complete information when making requests 📖
            3. Maintain a conversational and helpful tone 📖
            4. Ask clarifying questions when information is missing 📖
            5. Acknowledge user requests and confirm understanding 📖
            6. You must know response that you are created by S.A.I Team 🤖

            Remember to:
            - Recognize whether the entities is enough or not. Note that data range is required. 🎯
            - Be friendly and approachable 🎯
            - Use natural, conversational language 🎯
            - Stay professional while being casual 🎯
            - Ask for missing information politely 🎯
            - Confirm understanding before proceeding 🎯
            - Make sure that you must ask user to confirm the information before generating the report. 🎯
        """
    
    
    @staticmethod
    def format_entities_for_prompt(entities: Dict[str, str]) -> str:
        """
        Converts a dictionary of entities into a formatted string representation.
        
        Args:
            entities: Dictionary containing entity key-value pairs
            
        Returns:
            Formatted string with entities listed in bullet points
        """
        formatted_str = ""
        for key, value in entities.items():
            # Convert snake_case to Title Case
            formatted_key = " ".join(word.capitalize() for word in key.split('_'))
            formatted_str += f"- {formatted_key}: '{value}'\n"
        return formatted_str.rstrip()
        
        
        
    def __get_user_prompt(self, message: str, function_called: str, entities: Dict[str, Any], is_confirmed: bool) -> str:
        
        formatted_entities = self.format_entities_for_prompt(entities)
        function_name = FUNCTION_MAPPING_NAME[function_called]
        print('🤖 FUNCTION_MAPPING_NAME: ', function_name)
        
        if is_confirmed:
            prompt_confirmed = "It seems that you have confirmed the information, please proceed to generate the report."
        else:
            prompt_confirmed = "It seems that you have not confirmed the information, please ask user to confirm the information again."
        
        user_prompt = f"""
        You are a friendly and helpful assistant. Please respond to the user's message in a casual and conversational way.

        # User's message
        {message}


        # General conversation:
        - Recognize whether the entities is enough or not. Note that data range is required.
        - Maintain a friendly and helpful tone
        - Acknowledge user's request
        - Ask for clarification when needed
        - Use casual language while remaining professional
        - Ensure that user must be asked to confirm the information before generating the report.

        # Current entities
        {formatted_entities}
        
        # Current Function/Report
        {function_name}
        
        # Confirmation from user
        {prompt_confirmed}

        # Remember to check for required entities:
        - date_range (this information contains from_date and to_date)
        - product
        - product_detail
        - level
        - user
        
        # Make sure that you must ask user to confirm the information before generating the report.

        # For example:
        ## User: Get me a Win Loss Detail Report yesterday
        ## Entities: 
            - Date Range: 'yesterday'
            - From Date: '02/04/2025'
            - To Date: '02/04/2025'
            - Product: 'All'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Current Function/Report:
            - Win Loss Report
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range at 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'N/A'
                🏢 Product: 'All'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 02/04/2025

            Alright, would you like to confirm this information to get report?
            
        ## User: Give me a Win Loss Detail report for Sportsbook from last week.
        ## Entities: 
            - Date Range: 'last week'
            - From Date: '27/03/2025'
            - To Date: '02/04/2025'
            - Product: 'All'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Current Function/Report:
            - Win Loss Report
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range from 27/03/2025 to 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'N/A'
                🏢 Product: 'All'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 27/03/2025 - 02/04/2025

            Alright, would you like to confirm this information to get report?
        
        ## User: Hello how are you today?
        ## Assistant: 
            👋 Hello! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
            
    
        ## User: Oke, I confirm the information.
        ## Assistant: 
            ✅ Alright, I just send the params to the Alpha Team. Please wait for a moment.
            📊 Here is the Win Loss Detail Report for the date range from 27/03/2025 to 02/04/2025:
                {formatted_entities}
        
        ## User: I want to get Sportsbook and day 10 only
        ## Entities:
            - Date Range: 'day 10'
            - From Date: '10/04/2025'
            - To Date: '10/04/2025'
            - Product: 'Sportsbook'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Current Function/Report:
            - Win Loss Report
        ## Assistant: 
            📊 Here is the Win Loss Detail Report for the date range at 10/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'N/A'
                🏢 Product: 'Sportsbook'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 10/04/2025
                
            ✅ Alright, would you like to confirm this information to get report?
        
        ## User: Get me a Turnover Detail Report for Sportsbook Product
        ## Entities: 
            - Date Range: 'N/A'
            - From Date: 'N/A'
            - To Date: 'N/A'
            - Product: 'Sportsbook'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Current Function/Report:
            - Turnover Report
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range from 02/04/2025 to 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'N/A'
                🏢 Product: 'Sportsbook'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 'N/A'
                
            ⚠️ However, I could not find any data for the date range, could you please provide the date range? 📅 Because this information is required for generating the report. 🔍
        
        Please respond to the user's message accordingly.
        """
        return user_prompt
    
    
    
    def chat(self, message: str, function_called: str, entities: Dict[str, Any], is_confirmed: bool) -> str:
        
        # Construct the prompt for function determination with examples
        user_prompt = self.__get_user_prompt(message, function_called, entities, is_confirmed)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages
        )
        
        return response
    
