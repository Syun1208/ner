from typing import Any

from src.utils.utils import get_current_year, get_current_month, get_current_previous_date, get_last_week_dates, format_entities_for_prompt
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
    
        
        
    def __get_user_prompt(self, message: str, *args: Any) -> str:
        
        function_called = args[0]
        entities = args[1]
        is_confirmed = args[2]
        
        current_previous_date = get_current_previous_date()
        current_year = get_current_year()
        current_month = get_current_month()
        from_last_week_date, to_last_week_date = get_last_week_dates()

        formatted_entities = format_entities_for_prompt(entities)
        function_name = FUNCTION_MAPPING_NAME[function_called]
        
        if is_confirmed:
            prompt_confirmed = "⚠️ It seems that you have confirmed the information, please proceed to generate the report."
        else:
            prompt_confirmed = "❌ It seems that you have not confirmed the information, please ask user to confirm the information again."
        
        user_prompt = f"""
        You are a friendly and helpful assistant. Please respond to the user's message in a casual and conversational way.

        # User's message
        {message}


        # General conversation guidelines:
        - Check if all required entities are provided, especially date range 📅
        - Keep a friendly and helpful tone while staying professional 😊
        - Acknowledge and validate the user's request clearly 👍
        - Ask politely for any missing information ❓
        - Use natural, conversational language 💬
        - For report generation: Always ask for user confirmation. Once user confirms, that means is_confirmed=1, summarize the information and generate the report without asking for confirmation again ✅
        - Include relevant emojis when listing entities:
          * 📖 Requested by
          * 📅 Date Range
          * 📅 From Date
          * 📅 To Date
          * 🏢 Product
          * 📋 Product Detail  
          * 🎮 Level
          * 👤 User
        - If the current function/report is not found, you must response "I could not find the function/report, please give me a valid function/report" and ask user to provide the function/report again. Otherwise, you should let user know the current function/report that you are generating 📝 📊 📋
        - You must define which entity is not provided by user and ask user to confirm and provide the information ❓


        # Current entities
        {formatted_entities}
        
        # Current Function/Report
        {function_name}
        
        # Confirmation from user
        is_confirmed = {is_confirmed}
        {prompt_confirmed}

        # Remember to check for required entities:
        - date_range
        - from_date
        - to_date
        - product
        - product_detail
        - level
        - user
        
        # The language you must respond to user: ***English***


        # For example:
        ## User: Get me a Win Loss Detail Report yesterday
        ## Entities: 
            - Date Range: 'yesterday'
            - From Date: '{current_previous_date}/{current_month}/{current_year}'
            - To Date: '{current_previous_date}/{current_month}/{current_year}'
            - Product: 'All'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Current Function/Report:
            - Win Loss Report
        ## Confirmation from user
            - is_confirmed = 0
            - It seems that you have not confirmed the information, please ask user to confirm the information again.
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range at {current_previous_date}/{current_month}/{current_year}:
                📖 Report Requested by: 'All'
                📅 Date Range: 'yesterday'
                📅 From Date: {current_previous_date}/{current_month}/{current_year}
                📅 To Date: {current_previous_date}/{current_month}/{current_year}
                👤 Username: 'N/A'
                🏢 Product: 'All'
                📋 Product Detail: 'All'
                🎮 Level: 'All'

            ✅ Alright, would you like to confirm this information to get report?
            
            
        ## User: Give me a Win Loss Detail report for Sportsbook from last week.
        ## Entities: 
            - Date Range: 'last week'
            - From Date: '{from_last_week_date}'
            - To Date: '{to_last_week_date}'
            - Product: 'All'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Confirmation from user
            - is_confirmed = 0
            - It seems that you have not confirmed the information, please ask user to confirm the information again.
            
        ## Assistant:
            📊 Here is the Win Loss Detail Report for the date range from {from_last_week_date} to {to_last_week_date}:
                📖 Report Requested by: 'All'
                📅 Date Range: 'last week'
                📅 From Date: {from_last_week_date}
                📅 To Date: {to_last_week_date}
                👤 Username: 'N/A'
                🏢 Product: 'All'
                📋 Product Detail: 'All'
                🎮 Level: 'All'

            ✅ Alright, would you like to confirm this information to get report?
        
        
        ## User: Hello how are you today?
        ## Entities:
            - Date Range: 'N/A'
            - From Date: 'N/A'
            - To Date: 'N/A'
            - Product: 'N/A'
            - Product Detail: 'N/A'
            - Level: 'N/A'
            - User: 'N/A'
        ## Confirmation from user
            - is_confirmed = 0
            - It seems that you have not confirmed the information, please ask user to confirm the information again.
            
        ## Assistant: 
            👋 Hello! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
        
        
        ## User: I want to get Sportsbook and day 10 only
        ## Entities:
            - Date Range: 'day 10'
            - From Date: '10/{current_month}/{current_year}'
            - To Date: '10/{current_month}/{current_year}'
            - Product: 'Sportsbook'
            - Product Detail: 'All'
            - Level: 'All'
            - User: 'N/A'
        ## Confirmation from user
            - is_confirmed = 0
            - It seems that you have not confirmed the information, please ask user to confirm the information again.
            
        ## Assistant: 
            📊 Here is the Win Loss Detail Report for the date range at 10/04/2025:
                📖 Report Requested by: 'All'
                📅 Date Range: 'day 10'
                📅 From Date: 10/{current_month}/{current_year}
                📅 To Date: 10/{current_month}/{current_year}
                👤 Username: 'N/A'
                🏢 Product: 'Sportsbook'
                📋 Product Detail: 'All'
                🎮 Level: 'All'
                
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
        ## Confirmation from user
            - is_confirmed = 0
            - It seems that you have not confirmed the information, please ask user to confirm the information again.
            
        ## Assistant:
            📊 Here is the Turnover Detail Report:
                📖 Report Requested by: 'All'
                📅 Date Range: 'N/A'
                📅 From Date: 'N/A'
                📅 To Date: 'N/A'
                👤 Username: 'N/A'
                🏢 Product: 'Sportsbook'
                📋 Product Detail: 'All'
                🎮 Level: 'All'

            ⚠️ However, I could not find any data for the date range, could you please provide the date range? 📅 Because this information is required for generating the report. 🔍
        
        Please respond to the user's message accordingly.
        """
        return user_prompt
    
    
    
    def chat(self, message: str, *args: Any) -> str:
        
        # Construct the prompt for function determination with examples
        user_prompt = self.__get_user_prompt(message, *args)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages
        )
        
        return response
    
