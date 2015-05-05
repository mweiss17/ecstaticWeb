from django.contrib.gis.db import models
from django.conf import settings
import json

class location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    point = models.PointField(help_text="Represented as (longitude, latitude)")
    timestamp = models.DateTimeField("timestamp", auto_now=True)
    objects = models.GeoManager()
    class Meta:
		get_latest_by = "timestamp"

    def __unicode__(self):
        return json.dumps({"user":self.user.username, "point_lat":self.point.x, "point_lon":self.point.y, "timestamp":self.timestamp.isoformat()})