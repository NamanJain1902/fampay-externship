# from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Video
# from datetime import datetime


class JobScheduler():
    def __init__(self, obj) -> None:
        self.obj = obj
        self.eventId = str(hash(12332132132))
        self.scheduler = BackgroundScheduler()

    def __fetch(self):
        self.obj.update_table()

    def start(self):
        self.scheduler.add_job(self.__fetch, 'interval', seconds=10, id=self.eventId)
        self.scheduler.start()

    def stop(self):
        self.scheduler.remove_job(self.eventId)
