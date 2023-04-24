from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    # register the signals whenever this app is invoked
    def ready(self):
        import content.signals
