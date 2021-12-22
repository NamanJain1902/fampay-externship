from django.db import models


class VideoManager(models.Manager):
    def search_by_description(self, query):
        """
        Parameters
        -----------
            query : str 
                description to be searched.
       
        Returns
        -------
            video : list 
                list of matched query instances.
        """
        query = query.lower()
        filtered_videos = Video.objects.filter(description__icontains = query) 
        return filtered_videos

    def search_by_title(self, query):
        """
        Parameters
        -----------
            query : str
                title to be searched.
        
        Returns
        -------
            video : list
                list of matched query instances.
        """
        query = query.lower()
        filtered_videos =  Video.objects.filter(title__icontains = query) 
        return filtered_videos

    

class Video(models.Model):
    id = models.CharField(primary_key=True,max_length=100,null = False,blank=False)
    title = models.CharField(max_length=100,null = False, blank = False)
    description = models.TextField(null = True, blank = True)
    published_at = models.DateTimeField(null = False, blank = False)
    thumbnail_URL = models.URLField(max_length=500,null =False, blank = False)

    objects = VideoManager()

    class Meta:
        ordering = ('-published_at', )
