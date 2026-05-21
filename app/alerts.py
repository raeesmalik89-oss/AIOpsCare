# -----------------------------------
# AIOpsCare ICU Alert Engine
# -----------------------------------
# Detects abnormal patient conditions
# and generates ICU monitoring alerts


def generate_alerts(data):

    alerts = []

    # -----------------------------------
    # High Heart Rate Alert
    # -----------------------------------
    if data.heart_rate > 100:

        alerts.append(
            "High Heart Rate Detected"
        )

    # -----------------------------------
    # High Fever Alert
    # -----------------------------------
    if data.temperature > 38:

        alerts.append(
            "High Fever Detected"
        )

    # -----------------------------------
    # Respiratory Risk Alert
    # -----------------------------------
    if data.respiratory_rate > 24:

        alerts.append(
            "Abnormal Respiratory Rate"
        )

    # -----------------------------------
    # Return ICU Alerts
    # -----------------------------------
    return alerts