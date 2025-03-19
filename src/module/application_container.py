from dependency_injector import containers, providers
from thespian.actors import ActorSystem

from src.service.implement.arb_service_impl.arb_servive_impl import ARBServiceImpl
from src.service.interface.arb_service.arb_service import ARBService

from src.service.implement.arb_supporter_impl.normal_conversation_agent_impl import NormalConversationAgentImpl
from src.service.interface.arb_supporter.normal_conversation_agent import NormalConversationAgent


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

    arb_service = providers.AbstractSingleton(ARBService)
    arb_service.override(
        providers.Singleton(
            ARBServiceImpl,
            normal_conversation_agent = normal_conversation_agent
        )
    )
    
    