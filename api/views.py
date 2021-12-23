from django.http.response import HttpResponse
from .models import Video
from .serializers import VideoSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .pagination import VideoPagination


# Create your views here.
def index(request):
    return HttpResponse("Server Up !!")

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
