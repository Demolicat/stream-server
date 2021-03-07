from dependency_injector import containers, providers

from src.services.receiver_service import ReceiverService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    receiver_service = providers.Factory(ReceiverService)
