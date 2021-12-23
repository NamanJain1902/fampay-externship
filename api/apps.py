from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .jobs import JobScheduler
            from .query import query
            from .fetch_data import YoutubeAPI

            obj = YoutubeAPI(query=query)
            scheduler = JobScheduler(obj)
            obj.jobScheduler = scheduler
            scheduler.start()
