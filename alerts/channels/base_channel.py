from abc import ABC, abstractmethod
from alerts.models.user import User
from alerts.models.alert import Alert


class ChannelResult:
    """
    Represents the result of an alert channel operation.
    """
    def __init__(self, success: bool, info: str = ""):
        self.success = success
        self.info = info

    def __repr__(self):
        return f"ChannelResult(success={self.success}, info='{self.info}')"


class BaseChannel(ABC):
    """
    Abstract base class for alert channels.
    All alert channels should inherit from this class and implement the required methods.
    """

    @abstractmethod
    def send_alert(self, user: User, alert: Alert) -> ChannelResult:
        """
        Send an alert with the given message.

        :param user: The user to whom the alert is being sent.
        :param alert: The parameters to send the alert.
        :return: ChannelResult indicating success or failure of the operation.

        """
        raise NotImplementedError("Subclasses must implement this method.")
