from django.contrib.gis.db import models
from django.conf import settings

class location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    point = models.PointField(help_text="Represented as (longitude, latitude)")
    timestamp = models.DateTimeField("timestamp", auto_now=True)
    objects = models.GeoManager()
    class Meta:
		get_latest_by = "timestamp"

    def __unicode__(self):
        return self.user.username