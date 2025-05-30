from django.db.utils import IntegrityError
from django.test import TestCase


from alerts.models.alert import Alert
from alerts.models.sent_notification import SentNotification
from alerts.models.store import Store
from alerts.models.user import User
from alerts.models.user_alert_subscription import UserAlertSubscripion





class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", phone="1234567890", api_uid="uid123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.phone, "1234567890")
        self.assertEqual(self.user.api_uid, "uid123")
        self.assertEqual(str(self.user), "test@example.com")

    def test_user_unique_api_uid_constraint(self):
        self.assertRaises(
            IntegrityError,
            User.objects.create,
            email="second_user@example.com",
            api_uid=self.user.api_uid,
        )

    def test_user_unique_phone_constraint(self):
        self.assertRaises(
            IntegrityError,
            User.objects.create,
            email="second_user@example.com",
            phone=self.user.phone,
        )


class StoreModelTestCase(TestCase):
    def setUp(self):
        self.store = Store.objects.create(location="123 Main St", name="Test Store")

    def test_store_creation(self):
        self.assertEqual(self.store.location, "123 Main St")
        self.assertEqual(self.store.name, "Test Store")
        self.assertEqual(str(self.store), "Test Store")

    def test_store_location_as_primary_key(self):
        self.assertRaises(
            IntegrityError,
            Store.objects.create,
            location=self.store.location,
            name="Another Store",
        )


class AlertModelTestCase(TestCase):
    def setUp(self):
        self.store = Store.objects.create(location="123 Main St", name="Test Store")
        self.alert = Alert.objects.create(
            alert_uuid="123e4567-e89b-12d3-a456-426614174000",
            url="http://example.com/alert.jpg",
            location=self.store,
            label="theft",
            time_spotted=1622547800.0,
        )

    def test_alert_creation(self):
        self.assertEqual(self.alert.alert_uuid, "123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(self.alert.url, "http://example.com/alert.jpg")
        self.assertEqual(self.alert.location, self.store)
        self.assertEqual(self.alert.label, "theft")
        self.assertEqual(self.alert.time_spotted, 1622547800.0)
        self.assertEqual(
            str(self.alert),
            f"Alert for theft at {self.store} (123e4567-e89b-12d3-a456-426614174000)",
        )


class UserAlertSubscriptionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", phone="1234567890", api_uid="uid123")
        self.store = Store.objects.create(location="123 Main St", name="Test Store")
        self.subscription = UserAlertSubscripion.objects.create(
            user=self.user,
            store=self.store,
            alert_preference="standard",
            notification_channel="email",
        )

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.store, self.store)
        self.assertEqual(self.subscription.alert_preference, "standard")
        self.assertEqual(self.subscription.notification_channel, "email")
        self.assertEqual(
            str(self.subscription),
            f"{self.user.email} - {self.store.name} (standard) - email",
        )  

class SentNotificationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", phone="1234567890", api_uid="uid123")
        self.store = Store.objects.create(location="123 Main St", name="Test Store")
        self.alert = Alert.objects.create(
            alert_uuid="123e4567-e89b-12d3-a456-426614174000",
            url="http://example.com/alert.jpg",
            location=self.store,
            label="theft",
            time_spotted=1622547800.0,
        )
        self.sent_notification = SentNotification.objects.create(
            alert=self.alert,
            user=self.user,
            method="email",
            sent=True,
            sent_at="2024-06-01T12:00:00Z"
        )
    
    def test_sent_notification_creation(self):
        self.assertEqual(self.sent_notification.alert, self.alert)
        self.assertEqual(self.sent_notification.user, self.user)
        self.assertEqual(self.sent_notification.method, "email")
        self.assertTrue(self.sent_notification.sent)
        self.assertIsNotNone(self.sent_notification.sent_at)
        

                                        