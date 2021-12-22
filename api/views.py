from django.http.response import HttpResponse
from .models import Video
from .serializers import VideoSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .pagination import VideoPagination

from decouple import config, Csv
import time 
from .query import query
import requests
import json
from dateutil import parser
import threading


DEVELOPER_KEYS = config('DEVELOPER_KEY', cast=Csv())
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


# Create your views here.
def index(request):
    global key_idx
    return HttpResponse("Server Up !!")


def update_api_key_idx(self):
    print(self.apiKeyIndex)
    if self.apiKeyIndex < self.apiKeyIndexMaxValue:
      self.apiKeyIndex +=1

    else:
      self.apiKeyIndex = 0
      self.__update_try_count()


def load_data(attr):
    video = Video.objects.create(
        id = attr["id"]["videoId"], 
        title = attr["snippet"]["title"],
        description = attr["snippet"]["description"],
        thumbnail_URL = attr["snippet"]["thumbnails"]["default"]["url"],
        published_at = parser.parse(attr["snippet"]["publishedAt"])
    ),
    video.save()


def update_table():
    """Summary line.
    
    Server call the YouTube API continuously in background (async) with interval 10 seconds 
    for fetching the latest videos for a predefined search query and store the data of videos 
    (fields - Video title, description, publishing datetime, thumbnails URLs) 
    in a database with proper indexes.

    Support for supplying multiple API keys so that if quota is exhausted on one, it 
    automatically uses the next available key.
    """
    global key_idx
    key_idx = 0

    while True : 
        time.sleep(10)
        
        try : 
            key = DEVELOPER_KEYS[key_idx]
            url = f"https://youtube.googleapis.com/{YOUTUBE_API_SERVICE_NAME}/{YOUTUBE_API_VERSION}/search?part=snippet&q={query}&key={key}"

            global response
            response = requests.request("GET", url, headers={}, data={})
            data = json.loads(response.text)
            
            for item in data["items"]:
                if not Video.objects.filter(id = item["id"]["videoId"]).exists():
                    load_data(item)
                        
        except : 
            if(response.status_code == status.HTTP_403_FORBIDDEN):
                if key_idx + 1 < len(DEVELOPER_KEYS):
                    key_idx += 1
                else:
                    print("Parsed all keys!!! Max Quota Reached")
            else:
                print("Maximum Quota Reached")



class VideosView(viewsets.ModelViewSet):
    """Summary line.

    Utility to add pagitation in response.
    """
    queryset = Video.objects.all() 
    pagination_class = VideoPagination
    serializer_class = VideoSerializer 
    http_method_names = ['get']
   

class VideoQuery(APIView):
    """
    APIView is used because it allows developers to customize according to needs 
    and helps to scale API as required.
    """
    def get(self,request):
        """Summary line.

        A GET API which returns the stored video data in a paginated 
        response sorted in descending order of published datetime.

        Parameters
        -----------
            title : str 
                Title of video.
            
            description : str
                Video description.

        Returns
        -------
            VideoModel: Serialized video details for asked title/description
        """

        if 'description' in list(request.data.keys()) and 'title' in list(request.data.keys()):
            return Response({
                "message" : "Specify Only One field ! Either Description or Title"
            },status = status.HTTP_400_BAD_REQUEST)
       
        elif 'description' in list(request.data.keys()):
            videos = Video.objects.search_by_description(request.data["description"])
            serializer = VideoSerializer(videos, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        elif 'title' in list(request.data.keys()):
            videos = Video.objects.search_by_title(request.data["title"])
            serializer = VideoSerializer(videos, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response({
            "message" : "Neither of keys found description nor title"
        },status = status.HTTP_400_BAD_REQUEST)



t = threading.Thread(target=update_table)
t.start()
