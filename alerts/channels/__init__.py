from .api_channel import APIChannel


NOTIFICATION_CHANNELS = {
    "api": APIChannel(),
}

NOTIFICATION_CHANNEL_CHOICES = [
    (k, k.capitalize()) for k in NOTIFICATION_CHANNELS.keys()
]
