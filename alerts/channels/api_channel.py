import os

from dotenv import load_dotenv
from urllib3 import PoolManager, Retry
from urllib3.exceptions import MaxRetryError

from alerts.channels.base_channel import BaseChannel, ChannelResult
from alerts.models.user import User
from alerts.models.alert import Alert


load_dotenv()


class APIChannel(BaseChannel):
    """
    Channel for sending alerts via API.
    """

    def __init__(self):
        """
        Initialize the APIChannel.
        """
        self.retries = Retry(total=5, backoff_factor=1)
        self.http = PoolManager(retries=self.retries)
        self.api_hook_url = f"{os.getenv('ALERT_API_ROOT', 'http://localhost:8001/')}/webhook/notifications"

    def send_alert(self, user: User, alert: Alert) -> ChannelResult:
        """
        Send an alert with the given message via API.

        :param user: The user to whom the alert is being sent.
        :param alert: The parameters to send the alert.
        :return: ChannelResult indicating success or failure of the operation.
        """

        # Validate user parameters
        if not user or not isinstance(user, User):
            return ChannelResult(success=False, info="Invalid user")
        if user.api_uid is None:
            # User need to have an API UID to send alerts
            return ChannelResult(success=False, info="User does not have an API UID")

        # Validate alert parameters
        if not alert or not isinstance(alert, Alert):
            return ChannelResult(success=False, info="Invalid parameters for alert")

        # Prepare the API hook URL

        payload = {
            "url": alert.url,
            "alert_uuid": alert.alert_uuid,
            "location": alert.location.location,
            "label": alert.label,
            "target_user_id": user.api_uid,
        }

        api_timeout = int(os.getenv("ALERT_API_TIMEOUT", 5))

        # Send the alert via API
        try:
            response = self.http.request(
                "POST", self.api_hook_url, json=payload, timeout=api_timeout
            )
        except MaxRetryError as e:
            return ChannelResult(
                success=False,
                info=f"Failed to send alert {alert.alert_uuid}. No response from API: {self.api_hook_url}. Error: {str(e)}",
            )
        
        if response.status != 200:
            return ChannelResult(
                success=False,
                info=f"Failed to send alert {alert.alert_uuid}. Status: {response.status} - {response}",
            )

        return ChannelResult(
            success=True, info=f"Alert sent to {user.email}: {alert.alert_uuid}"
        )
