from django.apps import AppConfig


class TournamentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tournament'
    verbose_name = 'Torneo'

    def ready(self):
        import apps.tournament.signals  # noqa: F401