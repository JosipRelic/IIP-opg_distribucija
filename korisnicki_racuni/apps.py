from django.apps import AppConfig


class KorisnickiRacuniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'korisnicki_racuni'
    verbose_name = 'KORISNICKI RACUNI'

    def ready(self):
            import korisnicki_racuni.signals