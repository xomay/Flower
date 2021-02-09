from django.apps import AppConfig


class FlowerAppConfig(AppConfig):
    name = 'flower_app'

    def ready(self):
        import flower_app.email.mail_signal
