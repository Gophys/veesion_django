from django.db import models

from alerts.models.user import User
from alerts.models.alert import Alert


class SentNotification(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.alert} by {self.method} at {self.sent_at} - Susccess: {self.sent}"