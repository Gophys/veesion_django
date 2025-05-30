from django.db import models
from django.db.models.constraints import UniqueConstraint

from alerts.models.user import User
from alerts.models.store import Store
from alerts.channels import NOTIFICATION_CHANNEL_CHOICES

USER_ALERT_PREFERENCES = (
    ("standard", "Standard"),
    ("critical", "Critical"),
    ("both", "Both"),
)



class UserAlertSubscripion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    alert_preference = models.CharField(max_length=20, choices=USER_ALERT_PREFERENCES)
    notification_channel = models.CharField(max_length=50, choices=NOTIFICATION_CHANNEL_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.store.name} ({self.alert_preference}) - {self.notification_channel}"