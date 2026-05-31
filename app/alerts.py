# -----------------------------------
# AIOpsCare ICU Alert Engine
# -----------------------------------
# Detects abnormal patient conditions
# and generates ICU monitoring alerts


def generate_alerts(data):

    alerts = []

    # -----------------------------------
    # High Heart Rate Alert
    # --------------------------------
    if data.HR > 100:

        alerts.append(
            "High Heart Rate Detected"
        )

    # -----------------------------------
    # High Fever Alert
    # -----------------------------------
    if data.Temp > 38:

        alerts.append(
            "High Fever Detected"
        )

    # -----------------------------------
    # Respiratory Risk Alert
    # -----------------------------------
    if data.Resp > 24:

        alerts.append(
            "Abnormal Respiratory Rate"
        )

    # -----------------------------------
    # Return ICU Alerts
    # -----------------------------------
    return alerts
