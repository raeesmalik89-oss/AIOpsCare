
import os
import json
import requests
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

print(f"Listening on Kafka topic: {TOPIC}")

for message in consumer:
    record = message.value
    try:
        payload = {
            "HR":     float(record.get("HR", 0) or 0),
            "O2Sat":  float(record.get("O2Sat", 0) or 0),
            "Temp":   float(record.get("Temp", 0) or 0),
            "SBP":    float(record.get("SBP", 0) or 0),
            "MAP":    float(record.get("MAP", 0) or 0),
            "Resp":   float(record.get("Resp", 0) or 0),
            "Age":    float(record.get("Age", 0) or 0),
            "ICULOS": float(record.get("ICULOS", 0) or 0),
        }
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        result = response.json()
        patient_id = record.get("patient_id", "unknown")
        print(f"Patient {patient_id} -> Sepsis: {result['sepsis_prediction']} | Alerts: {result['alerts']}")
    except Exception as e:
        print(f"Error: {e}")
