from django.apps import AppConfig


class BeatcodeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beatcodeApp'

    def ready(self):
        from .update import start
        start()
