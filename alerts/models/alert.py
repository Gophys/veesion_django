from django.db import models
from alerts.models.store import Store


ALERT_LABELS = (

    ("theft", "theft"),
    ("suspicious", "suspicious"),
    ("normal", "normal"),
)


class Alert(models.Model):
    alert_uuid = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    location = models.ForeignKey(Store, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, choices=ALERT_LABELS)
    time_spotted = models.FloatField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.label} at {self.location} ({self.alert_uuid})"
