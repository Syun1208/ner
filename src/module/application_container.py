from dependency_injector import containers, providers
from thespian.actors import ActorSystem


from src.service.implement.arb_supporter_impl.greeting_agent import GreetingAgentImpl
from src.service.implement.arb_supporter_impl.normal_conversation_agent_impl import CasualConversationAgentImpl
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent


from src.service.interface.arb_supporter.llm import LLM
from src.service.implement.arb_supporter_impl.llm_impl import LLMImpl

from src.service.interface.arb_supporter.confirmation_agent import ConfirmationAgent
from src.service.implement.arb_supporter_impl.confirmation_agent_impl import ConfirmationAgentImpl
from src.service.implement.arb_supporter_impl.greeting_recognition_agent import GreetingRecognitionAgentImpl

from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.service.implement.arb_service_impl.arb_db_service_impl import ARBDBServiceImpl

from src.service.interface.arb_supporter.ner_agent import NerAgent
from src.service.implement.arb_supporter_impl.ner_agent_impl import NerAgentImpl

from src.service.interface.arb_supporter.function_calling_agent import FunctionCallingAgent
from src.service.implement.arb_supporter_impl.function_calling_extraction import FunctionCallingExtraction

from src.service.interface.arb_service.arb_service import ARBService
from src.service.implement.arb_service_impl.arb_servive_impl import ARBServiceImpl


class ApplicationContainer(containers.DeclarativeContainer):
    # Set up to get config 
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)

    arb_database = providers.AbstractSingleton(ARBDBService)
    arb_database.override(
        providers.Singleton(
            ARBDBServiceImpl,
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

    # casual_conversation_agent = providers.AbstractSingleton(NormalConversationAgent)
    # casual_conversation_agent.override(
    #     providers.Singleton(
    #         CasualConversationAgentImpl,
    #         llm
    #     )
    # )

    greeting_agent = providers.AbstractSingleton(NormalConversationAgent)
    greeting_agent.override(
        providers.Singleton(
            GreetingAgentImpl,
            llm=llm
        )
    )
    

    confirmation_agent = providers.AbstractSingleton(ConfirmationAgent)
    confirmation_agent.override(
        providers.Singleton(
            ConfirmationAgentImpl,
            llm=llm
        )
    )
    
    greeting_recognition_agent = providers.AbstractSingleton(ConfirmationAgent)
    greeting_recognition_agent.override(
        providers.Singleton(
            GreetingRecognitionAgentImpl,
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
    
    arb_service = providers.AbstractSingleton(ARBService)
    arb_service.override(
        providers.Singleton(
            ARBServiceImpl,
            casual_conversation_agent=greeting_agent,
            confirmation_agent=confirmation_agent,
            ner_agent=ner_agent,
            function_calling_agent=function_calling_agent,
            greeting_recognition_agent=greeting_recognition_agent,
            database=arb_database
        )
    )
    
    