ALERT_CLASSIFICATION = {
    "theft": "critical",
    "suspicious": "standard",
    "normal": "standard",
}

def get_alert_classification(label):
    """
    Returns the classification of the alert based on its label.
    """
    return ALERT_CLASSIFICATION.get(label.lower(), "standard")
    