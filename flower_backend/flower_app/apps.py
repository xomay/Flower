from django.apps import AppConfig


class FlowerAppConfig(AppConfig):
    name = 'flower_app'

    def ready(self):
        import flower_app.email.mail_signal
        ParamsJEModel = self.get_model('ParamsJE')
        GLOBAL_PARAMS_JE = ParamsJEModel.objects.get(pk=1)
        if(GLOBAL_PARAMS_JE == None):
            print("ALERT : Don't forget to initialize an instance of ParamsJE.")