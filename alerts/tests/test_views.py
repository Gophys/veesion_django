import time
from unittest import mock
from django.test import TestCase

from alerts.models.alert import Alert
from alerts.models.sent_notification import SentNotification
from alerts.models.store import Store
from alerts.models.user import User
from alerts.models.user_alert_subscription import UserAlertSubscripion

from django.urls import reverse
from rest_framework import status


class AlertWebhookViewTestCase(TestCase):

    def setUp(self):
        self.store = Store.objects.create(location="test-store", name="Test Store")
        self.user = User.objects.create(
            email="test@user.com", phone="1234567890", api_uid="test_api_uid"
        )
    
    @mock.patch("alerts.channels.api_channel.APIChannel.send_alert")
    def test_post_valid_alert(self, mock_send_alert):
        url = reverse("alert-webhook")
        # Create a user alert subscription
        UserAlertSubscripion.objects.create(
            user=self.user,
            store=self.store,
            alert_preference="both",
            notification_channel="api",
        )
        data = {
            "url": "http://example.com/alert",
            "location": self.store.location,
            "alert_uuid": "test-alert-uuid",
            "label": "theft",
            "time_spotted": 1234567890.0,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Alert.objects.filter(alert_uuid="test-alert-uuid").exists())
        alert = Alert.objects.get(alert_uuid="test-alert-uuid")
        self.assertEqual(alert.url, "http://example.com/alert")
        self.assertEqual(alert.location, self.store)
        self.assertEqual(alert.label, "theft")
        self.assertEqual(alert.time_spotted, 1234567890.0)
        sent_alert = SentNotification.objects.filter(alert=alert).first()
        self.assertIsNotNone(sent_alert)
        self.assertEqual(sent_alert.user, self.user)
        self.assertEqual(sent_alert.method, "api")
        self.assertTrue(mock_send_alert.called)
    

    def test_post_existing_alert(self):
        alert = Alert.objects.create(
            alert_uuid="existing-alert-uuid",
            url="http://example.com/existing",
            location=self.store,
            label="theft",
            time_spotted=1234567890.0,
        )
        url = reverse("alert-webhook")
        data = {
            "url": "http://example.com/alert",
            "location": self.store.location,
            "alert_uuid": "existing-alert-uuid",
            "label": "theft",
            "time_spotted": 1234567890.0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_data(self):
        url = reverse("alert-webhook")
        data = {
            "url": "http://example.com/alert",
            "location": self.store.location,
            "alert_uuid": "test-alert-uuid",
            # Missing 'label' and 'time_spotted'
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("label", response.data)
        self.assertIn("time_spotted", response.data)

    def test_post_invalid_location(self):
        url = reverse("alert-webhook")
        data = {
            "url": "http://example.com/alert",
            "location": "invalid-location",
            "alert_uuid": "test-alert-uuid",
            "label": "theft",
            "time_spotted": 1234567890.0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("location", response.data)

    def test_post_no_subscriptions(self):
        url = reverse("alert-webhook")
        data = {
            "url": "http://example.com/alert",
            "location": self.store.location,
            "alert_uuid": "test-alert-uuid",
            "label": "theft",
            "time_spotted": 1234567890.0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"status": "No user subscriptions found"})

    @mock.patch("alerts.channels.api_channel.APIChannel.send_alert")
    def test_post_mulitple_subscriptions(self, mock_send_alert):
        # Create a user alert subscription
        UserAlertSubscripion.objects.create(
            user=self.user,
            store=self.store,
            alert_preference="both",
            notification_channel="api",
        )
        UserAlertSubscripion.objects.create(
            user=self.user,
            store=self.store,
            alert_preference="both",
            notification_channel="email",
        )

        url = reverse("alert-webhook")
        data = {
            "url": "http://example.com/alert",
            "location": self.store.location,
            "alert_uuid": "test-alert-uuid",
            "label": "theft",
            "time_spotted": 1234567890.0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Alert.objects.filter(alert_uuid="test-alert-uuid").exists())

        # Check that two notifications were created       
        notifications = SentNotification.objects.all()
        self.assertEqual(len(notifications), 2)
        for notification in notifications:
            self.assertEqual(notification.alert.alert_uuid, "test-alert-uuid")
            if notification.method == "api":
                self.assertTrue(notification.sent)
            elif notification.method == "email":
                # Email channel is not implemented in this test, so it should not be sent
                self.assertFalse(notification.sent)



