from django.test import TestCase
from unittest.mock import MagicMock

from alerts.models.alert import Alert
from alerts.models.store import Store
from alerts.models.user import User

from alerts.channels.api_channel import APIChannel
from alerts.channels.base_channel import ChannelResult


class UserModelTestCase(TestCase):
    def setUp(self):
        self.api_channel = APIChannel()
        self.user = User.objects.create(
            email="test@test.com",
            phone="1234567890",
            api_uid="test_api_uid",
        )
        self.store = Store.objects.create(location="test-location", name="Test Store")

        self.alert = Alert.objects.create(
            location=self.store,
            alert_uuid="test-alert-uuid",
            label="Test Alert",
            time_spotted=1111.11,
        )

        self.api_channel.http = MagicMock()

    def test_send_notification_success(self):
        self.api_channel.http.request.return_value = MagicMock(
            status=200, data=b'{"success": true}'
        )

        response = self.api_channel.send_alert(self.user, self.alert)
        self.api_channel.http.request.assert_called_once_with(
            "POST",
            self.api_channel.api_hook_url,
            json={
                "url": "",
                "alert_uuid": "test-alert-uuid",
                "location": "test-location",
                "label": "Test Alert",
                "target_user_id": "test_api_uid",
            },
            timeout=5,
        )
        self.assertIsInstance(response, ChannelResult)
        self.assertTrue(response.success)

    def test_send_notification_none_user(self):
        invalid_user = None
        response = self.api_channel.send_alert(invalid_user, self.alert)
        self.assertIsInstance(response, ChannelResult)
        self.assertFalse(response.success)
        self.assertEqual(response.info, "Invalid user")
    
    def test_send_notification_not_a_user(self):
        invalid_user = "not_a_user"
        response = self.api_channel.send_alert(invalid_user, self.alert)
        self.assertIsInstance(response, ChannelResult)
        self.assertFalse(response.success)
        self.assertEqual(response.info, "Invalid user")

    def test_send_user_notification_no_api_uid(self):
        user_without_api_uid = User.objects.create(
            email="test@api_no_uid.com", phone="no_uid_phone", api_uid=None
        )
        response = self.api_channel.send_alert(user_without_api_uid, self.alert)
        self.assertIsInstance(response, ChannelResult)
        self.assertFalse(response.success)
        self.assertEqual(response.info, "User does not have an API UID")

    def test_send_notification_none_alert(self):
        invalid_alert = None
        response = self.api_channel.send_alert(self.user, invalid_alert)
        self.assertIsInstance(response, ChannelResult)
        self.assertFalse(response.success)
        self.assertEqual(response.info, "Invalid parameters for alert")

    def test_send_notification_not_an_alert(self):
        invalid_alert = "not_an_alert"
        response = self.api_channel.send_alert(self.user, invalid_alert)
        self.assertIsInstance(response, ChannelResult)
        self.assertFalse(response.success)
        self.assertEqual(response.info, "Invalid parameters for alert")
