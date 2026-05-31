
import json
import os
import joblib

MODEL_PATH = os.getenv("MODEL_PATH", "/app/ml/model.joblib")

HEART_RATE_THRESHOLD = 100
TEMP_THRESHOLD = 38.0
RR_THRESHOLD = 24
O2SAT_THRESHOLD = 95
SBP_THRESHOLD = 90
MAP_THRESHOLD = 65

model = joblib.load(MODEL_PATH)

def handle(event, context):
    try:
        body = json.loads(event.body)
        HR     = float(body["HR"])
        O2Sat  = float(body["O2Sat"])
        Temp   = float(body["Temp"])
        SBP    = float(body["SBP"])
        MAP    = float(body["MAP"])
        Resp   = float(body["Resp"])
        Age    = float(body["Age"])
        ICULOS = float(body["ICULOS"])

        prediction = int(model.predict([[HR, O2Sat, Temp, SBP, MAP, Resp, Age, ICULOS]])[0])

        alerts = []
        if HR > HEART_RATE_THRESHOLD:
            alerts.append("High Heart Rate Detected")
        if Temp > TEMP_THRESHOLD:
            alerts.append("High Fever Detected")
        if Resp > RR_THRESHOLD:
            alerts.append("Abnormal Respiratory Rate")
        if O2Sat < O2SAT_THRESHOLD:
            alerts.append("Low Oxygen Saturation")
        if SBP < SBP_THRESHOLD:
            alerts.append("Low Systolic Blood Pressure")
        if MAP < MAP_THRESHOLD:
            alerts.append("Low Mean Arterial Pressure")

        return {
            "statusCode": 200,
            "body": json.dumps({"sepsis_prediction": prediction, "alerts": alerts}),
        }
    except (KeyError, ValueError) as e:
        return {"statusCode": 400, "body": json.dumps({"error": f"Invalid input: {e}"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
