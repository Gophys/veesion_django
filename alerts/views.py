import logging
import threading

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from alerts.channels import NOTIFICATION_CHANNELS
from alerts.alerts import get_alert_classification
from alerts.models.alert import Alert
from alerts.models.store import Store
from alerts.models.sent_notification import SentNotification
from alerts.models.user import User
from alerts.models.user_alert_subscription import UserAlertSubscripion


from alerts.serializers import (
    AlertSerializer,
    UserSerializer,
    StoreSerializer,
    UserAlertSubscriptionSerializer,
    SentNotificationSerializer,
)


logger = logging.getLogger(__name__)


class AlertWebhookView(CreateAPIView):
    """
    View to handle incoming alerts via webhook.
    This view processes the alert data, checks user preferences, and sends notifications.
    """

    # serializer_class is used to validate the incoming data and show the html representation of the data
    serializer_class = AlertSerializer

    def post(self, request, *args, **kwargs):

        logger.info(f"Received alert data: {request.data}")

        # Validate the incoming request data
        serializer = AlertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Process the alert data
        alert_data = serializer.validated_data

        # Create or get the alert instance
        alert = Alert.objects.create(
            alert_uuid=alert_data["alert_uuid"],
            url=alert_data["url"],
            location=alert_data["location"],
            label=alert_data["label"],
            time_spotted=alert_data["time_spotted"],
        )

        # Get all the subscriptions for the store and alert preference based on the alert label
        severity = get_alert_classification(alert.label)
        severity_filter = [severity, "both"]
        user_alert_subscriptions = UserAlertSubscripion.objects.filter(
            store=alert.location, alert_preference__in=severity_filter
        ).prefetch_related("user")

        if not user_alert_subscriptions:
            logger.info(
                f"No user subscriptions found for store {alert.location} with alert preference {severity_filter}."
            )
            return Response(
                {"status": "No user subscriptions found"},
                status=status.HTTP_204_NO_CONTENT,
            )
        
       
        # This method should be called in a separate thread to avoid blocking the request, but is currently called directly
        self.send_alerts(alert, user_alert_subscriptions)

        return Response({"status": "Alert correctly received"}, status=status.HTTP_200_OK)
    
    def send_alerts(self, alert: Alert, user_alert_subscriptions: list[UserAlertSubscripion]):
        """
        Send alerts to all users subscribed to the store and alert preference.
        This method is called in a separate thread to avoid blocking the request.
        """
        for subscription in user_alert_subscriptions:
            # Create the SentNotification instance
            # Initially set sent to False, it will be updated after sending the notification
            sent_notification = SentNotification.objects.create(
                alert=alert,
                user=subscription.user,
                method=subscription.notification_channel,
                sent_at=timezone.now(),
                sent=False,
            )
        
            channel = NOTIFICATION_CHANNELS.get(subscription.notification_channel)
            if not channel:
                logger.error(
                    f"Notification channel {subscription.notification_channel} not found for user {subscription.user.email}."
                )
                continue

            # Send the alert using the specified channel
            result = channel.send_alert(
                subscription.user,
                alert,
            )

            # Log the result of the notification attempt
            if result.success:
                logger.info(
                    f"Alert sent successfully to {subscription.user.email} via {subscription.notification_channel}."
                )
                sent_notification.sent = True
                sent_notification.save()
            else:
                logger.error(
                    f"Failed to send alert to {subscription.user.email} via {subscription.notification_channel}: {result.info}"
                )


# API Views for listing and creating resources (these are used to fill the tables using the browser version of the API)
class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StoreListView(ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class UserAlertSubscriptionListView(ListCreateAPIView):
    queryset = UserAlertSubscripion.objects.all()
    serializer_class = UserAlertSubscriptionSerializer


class SentNotificationListView(ListAPIView):
    queryset = SentNotification.objects.all()
    serializer_class = SentNotificationSerializer


class AlertListView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer