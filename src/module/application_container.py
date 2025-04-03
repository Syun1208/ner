from dependency_injector import containers, providers
from thespian.actors import ActorSystem


from src.service.implement.arb_supporter_impl.normal_conversation_agent_impl import CasualConversationAgentImpl
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent

from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.llm_impl import LLMImpl

from src.service.interface.arb_supporter.confirmation_agent import ConfirmationAgent
from src.service.implement.arb_supporter_impl.confirmation_agent_impl import ConfirmationAgentImpl

from src.service.interface.arb_supporter.nosql_dabase import NoSQLDatabase
from src.service.implement.arb_supporter_impl.json_database import JsonDatabase

from src.service.interface.arb_supporter.ner_agent import NerAgent
from src.service.implement.arb_supporter_impl.ner_agent_impl import NerAgentImpl

from src.service.interface.arb_supporter.function_calling_agent import FunctionCallingAgent
from src.service.implement.arb_supporter_impl.function_calling_extraction import FunctionCallingExtraction

from src.service.interface.arb_supporter.multi_agent import MultiAgent
from src.service.implement.arb_supporter_impl.predator_chatbot import PredatorChatbot


class ApplicationContainer(containers.DeclarativeContainer):
    # Set up to get config 
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)

    arb_database = providers.AbstractSingleton(NoSQLDatabase)
    arb_database.override(
        providers.Singleton(
            JsonDatabase,
            database_path=config.database.database_path
        )
    )

    llm = providers.AbstractSingleton(LLM)
    llm.override(
        providers.Singleton(
            LLMImpl,
            api=config.llm.api,
            model=config.llm.model
        )
    )

    casual_conversation_agent = providers.AbstractSingleton(NormalConversationAgent)
    casual_conversation_agent.override(
        providers.Singleton(
            CasualConversationAgentImpl,
            llm
        )
    )

    
    confirmation_agent = providers.AbstractSingleton(ConfirmationAgent)
    confirmation_agent.override(
        providers.Singleton(
            ConfirmationAgentImpl,
            llm=llm
        )
    )
    
    ner_agent = providers.AbstractSingleton(NerAgent)
    ner_agent.override(
        providers.Singleton(
            NerAgentImpl,
            llm=llm
        )
    )
    
    function_calling_agent = providers.AbstractSingleton(FunctionCallingAgent)
    function_calling_agent.override(
        providers.Singleton(
            FunctionCallingExtraction,
            llm=llm
        )
    )
    
    arb_service = providers.AbstractSingleton(MultiAgent)
    arb_service.override(
        providers.Singleton(
            PredatorChatbot,
            casual_conversation_agent=casual_conversation_agent,
            confirmation_agent=confirmation_agent,
            ner_agent=ner_agent,
            function_calling_agent=function_calling_agent,
            database=arb_database
        )
    )
    
    