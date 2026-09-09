from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    # the signal will only be executed if i import it here
    def ready(self) -> None:
        import core.signals.handlers
