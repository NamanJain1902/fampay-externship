from .models import Video
from rest_framework import status

from decouple import config, Csv
import requests
import json
from dateutil import parser


DEVELOPER_KEYS = config('DEVELOPER_KEY', cast=Csv())
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
BASE_URL = "https://youtube.googleapis.com"


class YoutubeAPI:

    def __init__(self, query="google", jobScheduler=None) -> None:
        self.query = query
        self.key_idx = 0
        self.jobScheduler = jobScheduler

    def __update_api_key_idx(self):
        if self.key_idx < len(DEVELOPER_KEYS):
            self.key_idx +=1
            return True
        else:
            return False


    def __load_data(self, attr):
        """Summary line.

        Save fetched item to Video table.
        """
        video = Video.objects.create(
            id = attr["id"]["videoId"], 
            title = attr["snippet"]["title"],
            description = attr["snippet"]["description"],
            thumbnail_URL = attr["snippet"]["thumbnails"]["default"]["url"],
            published_at = parser.parse(attr["snippet"]["publishedAt"])
        ),
        video.save()


    def update_table(self):
        """Summary line.
        
        Server call the YouTube API continuously in background (async) with interval 10 seconds 
        for fetching the latest videos for a predefined search query and store the data of videos 
        (fields - Video title, description, publishing datetime, thumbnails URLs) 
        in a database with proper indexes.

        Support for supplying multiple API keys so that if quota is exhausted on one, it 
        automatically uses the next available key.
        """

        try : 
            key = DEVELOPER_KEYS[self.key_idx]
            
            url = f"{BASE_URL}/{YOUTUBE_API_SERVICE_NAME}/{YOUTUBE_API_VERSION}/search?part=snippet&q={self.query}&key={key}"

            global response
            response = requests.request("GET", url, headers={}, data={})
            data = json.loads(response.text)
            for item in data["items"]:
                if not Video.objects.filter(id = item["id"]["videoId"]).exists():
                    self.__load_data(item)
                        
        except : 
            if(response.status_code == status.HTTP_403_FORBIDDEN):
                if self.__update_api_key_idx() == True:
                    self.update_table()
                else:
                    self.jobScheduler.stop()
                    print("Maximum Quota Reached")
            