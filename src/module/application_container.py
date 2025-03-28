from dependency_injector import containers, providers
from thespian.actors import ActorSystem

from src.service.implement.arb_service_impl.arb_servive_impl import ARBServiceImpl
from src.service.interface.arb_service.arb_service import ARBService

from src.service.implement.arb_supporter_impl.normal_conversation_agent_impl import NormalConversationAgentImpl
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent

from src.service.interface.arb_supporter.function_calling_conversation_agent import FunctionCallingConversationAgent
from src.service.implement.arb_supporter_impl.function_calling_conversation_agent_impl import FunctionCallingConversationAgentImpl
class ApplicationContainer(containers.DeclarativeContainer):
    # set up to get config 
    config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)

    normal_conversation_agent = providers.AbstractSingleton(NormalConversationAgent)
    normal_conversation_agent.override(
        providers.Singleton(
            NormalConversationAgentImpl,
            history_context_folder=config.data_path.history_context_folder,
            normal_conversation_agent_config=config.normal_conversation_agent
        )
    )

    function_calling_conversation_agent = providers.AbstractSingleton(FunctionCallingConversationAgent)
    function_calling_conversation_agent.override(
        providers.Singleton(
            FunctionCallingConversationAgentImpl,
            history_context_folder=config.data_path.history_context_folder,
            function_calling_conversation_agent_config=config.function_calling_conversation_agent
        )
    )


    arb_service = providers.AbstractSingleton(ARBService)
    arb_service.override(
        providers.Singleton(
            ARBServiceImpl,
            normal_conversation_agent = normal_conversation_agent,
            function_calling_conversation_agent = function_calling_conversation_agent
        )
    )
    
    