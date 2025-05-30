from rest_framework import serializers

from alerts.models.alert import Alert
from alerts.models.sent_notification import SentNotification
from alerts.models.store import Store
from alerts.models.user import User
from alerts.models.user_alert_subscription import UserAlertSubscripion


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['url', 'location', 'alert_uuid', 'label', 'time_spotted']


# The serializers below are used to facilitate the filling of the tables using the browser versionof the api.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'api_uid']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['location', 'name']

class UserAlertSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlertSubscripion
        fields = ['user', 'store', 'alert_preference', 'notification_channel']

class SentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentNotification
        fields = ['alert', 'user', 'method', 'sent', 'sent_at']

