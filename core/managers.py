from django.db import models
class ContentManager( models.Manager ):
    def get_query_set(self):
        queryset = super( ContentManager , self ).get_query_set()
        queryset = queryset.filter( hidden = False ).order_by("-publish_date")
      
        return queryset