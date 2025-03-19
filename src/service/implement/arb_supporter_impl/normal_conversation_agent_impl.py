import os
from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.memory.buffer import ConversationBufferMemory
from langchain.memory.chat_message_histories.file import FileChatMessageHistory

from src.utils.constants import Prompt as p

class NormalConversationAgentImpl:
    def __init__(self, history_context_folder: str, normal_conversation_agent_config:dict):
        self.history_context_folder = history_context_folder
        self.normal_conversation_agent_config = normal_conversation_agent_config
        if not os.path.exists(self.history_context_folder):
            os.makedirs(self.history_context_folder)


        self.__get_llm()
        self.__get_chat_prompt_template()
        

    def __get_llm(self):
        self.llm = Ollama(base_url= self.normal_conversation_agent_config['llm_api_url'], 
                            model = self.normal_conversation_agent_config['model'], 
                            temperature = self.normal_conversation_agent_config['temperature'],)
        
    
    def __get_chat_prompt_template(self):
        self.prompt = ChatPromptTemplate(input_variables=["content", "messages"],
                                         messages=[
                                             SystemMessagePromptTemplate.from_template(p.NORMAL_CONVERSATION_AGENT_PROMT),
                                             MessagesPlaceholder(variable_name="messages"),
                                             HumanMessagePromptTemplate.from_template("{content}"),
                                             ],
                                             )
    
    def __get_memory(self, history_context_path: str):
        self.memory =  ConversationBufferMemory(
            memory_key="messages",
            chat_memory=FileChatMessageHistory(file_path=history_context_path),
            return_messages=True,
            input_key="content",
        )
    
    def __create_chain(self):
        self.conversation_chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)
    
    def start_conversation(self, user_id: int, session_id: str) -> None:
        history_context_path = os.path.join(self.history_context_folder, str(user_id) + "_" + session_id + ".json")
        self.__get_memory(history_context_path)
        self.__create_chain()

    def end_conversation(self, user_id: int, session_id: str) -> None:
        history_context_path = os.path.join(self.history_context_folder, str(user_id) + "_" + session_id + ".json")
        if os.path.exists(history_context_path):
            os.remove(history_context_path)

    def responding(self, user_id: int, session_id: str, message: str) -> str:
        history_context_path = os.path.join(self.history_context_folder, str(user_id) + "_" + session_id + ".json")

        if not os.path.exists(history_context_path):
            self.start_conversation(user_id, session_id)

        return self.conversation_chain.invoke({"content": message})

    

    