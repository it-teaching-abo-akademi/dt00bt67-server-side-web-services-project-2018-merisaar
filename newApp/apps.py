from django.apps import AppConfig


class NewappConfig(AppConfig):
    name = 'newApp'

    def ready(self):
        import newApp.signals
