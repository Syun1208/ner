from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent
from src.service.interface.arb_supporter.llm import LLM

class GreetingAgentImpl(NormalConversationAgent):
    
    def __init__(
        self, 
        llm: LLM
    ) -> None:
        self.llm = llm
        self.system_prompt = """
            You are a friendly and helpful S.A.I's Assistant trained to greet user.

            Your main responsibilities are:
            1. Maintain a conversational and helpful tone 📖
            2. You must know response that you are created by S.A.I Team 🤖

            Remember to:
            - Be friendly and approachable 🎯
            - Use natural, conversational language 🎯
            - Stay professional while being casual 🎯
        """
       
        
    def __get_user_prompt(self, message: str) -> str:
        
        user_prompt = f"""

        # User's message
        {message}


        # General conversation guidelines:
        - Keep a friendly and helpful tone while staying professional 😊
        - Acknowledge and validate the user's request clearly 👍
        - Use natural, conversational language 💬
        
        # The language you must respond to user: ***English***


        # For example:
        ## User: Hello how are you today?  
        ## Assistant: 
            👋 Hello! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
        
        ## User: Hi, I'm John Doe.
        ## Assistant: 
            👋 Hello John Doe! I'm a 🤖 friendly and helpful assistant from S.A.I Team. How can I assist you today? 😊
            
        ## User: Bye see you again.
        ## Assistant: 
            👋 Goodbye! Have a great day! 😊, this is S.A.I's Assistant. See you next time! 👋
        """
        return user_prompt
    
    
    
    def chat(self, message: str) -> str:
        
        # Construct the prompt for function determination with examples
        user_prompt = self.__get_user_prompt(message)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages
        )
        
        return response
    
