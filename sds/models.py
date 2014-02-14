from django.db import models
import datetime

class Photos(models.Model):
    url = models.CharField(max_length=100)
    user_id = models.CharField(max_length=30)
    photographer = models.CharField(max_length=30)
    
    @classmethod
    def create(cls, url, user_id, photographer):
        image = cls(url=url, user_id=user_id, photographer=photographer)
        return image
