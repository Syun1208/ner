from typing import Dict, Any

from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
from src.service.interface.arb_supporter.llm import LLM


class CasualConversationAgentImpl(NormalConversationAgent):
    
    def __init__(
        self, 
        llm: LLM
    ) -> None:
        self.llm = llm
        self.system_prompt = """
            You are a friendly and helpful assistant trained to handle conversations about Win/Loss reports and other queries in a casual yet professional manner.

            Your main responsibilities are:
            1. Help users get the information they need about Win/Loss reports
            2. Guide users to provide complete information when making requests
            3. Maintain a conversational and helpful tone
            4. Ask clarifying questions when information is missing
            5. Acknowledge user requests and confirm understanding

            Remember to:
            - Recognize whether the entities is enough or not. Note that data range is required.
            - Be friendly and approachable
            - Use natural, conversational language
            - Stay professional while being casual
            - Ask for missing information politely
            - Confirm understanding before proceeding
            - Make sure that you must ask user to confirm the information before generating the report.
        """
    
    
    
    def __format_entities_for_prompt(entities: Dict[str, str]) -> str:
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
            formatted_str += f"        - {formatted_key}: '{value}'\n"
        return formatted_str.rstrip()
        
        
        
    def __get_user_prompt(self, message: str, entities: Dict[str, Any]) -> str:
        
        formatted_entities = self.__format_entities_for_prompt(entities)
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
            - User: 'All'
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range at 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'All'
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
            - User: 'All'
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range from 27/03/2025 to 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'All'
                🏢 Product: 'All'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 27/03/2025 - 02/04/2025

            Alright, would you like to confirm this information to get report?
        
        ## User: Hello how are you today?
        ## Assistant: 
            👋 Hello! I'm a 🤖 friendly and helpful assistant. How can I assist you today? 😊
        
        
        ## User: Get me a Turnover Detail Report for Sportsbook Product
        ## Entities: 
            - Date Range: 'N/A'
            - From Date: 'N/A'
            - To Date: 'N/A'
            - Product: 'Sportsbook'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'All'
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range from 02/04/2025 to 02/04/2025:
                📖 Report Requested by: 'All'
                👤 Username: 'All'
                🏢 Product: 'Sportsbook'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                📅 Date Range: 'N/A'
                
            ⚠️ However, I could not find any data for the date range, could you please provide the date range? 📅 Because this information is required for generating the report. 🔍
        
        Please respond to the user's message accordingly.
        """
        return user_prompt
    
    
    
    def chat(self, message: str, entities: Dict[str, Any]) -> str:
        
        # Construct the prompt for function determination with examples
        user_prompt = self.__get_user_prompt(message, entities)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages
        )
        
        return response
    
