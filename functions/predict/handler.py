import json
import joblib
import os

MODEL_PATH = os.getenv("MODEL_PATH", "/app/ml/model.joblib")
HEART_RATE_THRESHOLD = 100
TEMP_THRESHOLD = 38.0
RR_THRESHOLD = 24

model = joblib.load(MODEL_PATH)


def handle(event, context):
    try:
        body = json.loads(event.body)
        heart_rate = float(body["heart_rate"])
        temperature = float(body["temperature"])
        respiratory_rate = float(body["respiratory_rate"])

        prediction = int(model.predict([[heart_rate, temperature, respiratory_rate]])[0])

        alerts = []
        if heart_rate > HEART_RATE_THRESHOLD:
            alerts.append("High Heart Rate Detected")
        if temperature > TEMP_THRESHOLD:
            alerts.append("High Fever Detected")
        if respiratory_rate > RR_THRESHOLD:
            alerts.append("Abnormal Respiratory Rate")

        return {
            "statusCode": 200,
            "body": json.dumps({"sepsis_prediction": prediction, "alerts": alerts}),
        }
    except (KeyError, ValueError) as e:
        return {"statusCode": 400, "body": json.dumps({"error": f"Invalid input: {e}"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
