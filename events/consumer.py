
import os, json, requests
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "patient-vitals"
API_URL = "http://localhost:8000/predict"
TOKEN = "testtoken"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="aiopscare-consumer"
)

def safe_float(val):
    try:
        f = float(val)
        return 0.0 if (f != f) else f
    except (TypeError, ValueError):
        return 0.0

print(f"Listening on Kafka topic: {TOPIC}")

for message in consumer:
    record = message.value
    try:
        payload = {
            "HR":     safe_float(record.get("HR")),
            "O2Sat":  safe_float(record.get("O2Sat")),
            "Temp":   safe_float(record.get("Temp")),
            "SBP":    safe_float(record.get("SBP")),
            "MAP":    safe_float(record.get("MAP")),
            "Resp":   safe_float(record.get("Resp")),
            "Age":    safe_float(record.get("Age")),
            "ICULOS": safe_float(record.get("ICULOS")),
        }
        response = requests.post(API_URL, json=payload,
            headers={"Authorization": f"Bearer {TOKEN}"})
        result = response.json()
        patient_id = record.get("patient_id", "unknown")
        print(f"Patient {patient_id} -> Sepsis: {result['sepsis_prediction']} | Alerts: {result['alerts']}")
    except Exception as e:
        print(f"Error: {e}")
