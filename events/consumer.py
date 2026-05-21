import os
import json
import httpx
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
OPENFAAS_URL = os.getenv("OPENFAAS_URL", "http://openfaas-gateway:8080")
FUNCTION_ENDPOINT = f"{OPENFAAS_URL}/function/sepsis-predict"

consumer = KafkaConsumer(
    "patient-events",
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Consumer listening — forwarding events to OpenFaaS predict function...")

for message in consumer:
    patient_data = message.value
    print(f"\nReceived event: {patient_data}")

    try:
        response = httpx.post(FUNCTION_ENDPOINT, json=patient_data, timeout=10.0)
        result = response.json()
        print(f"Prediction: {result['sepsis_prediction']}")
        if result.get("alerts"):
            print(f"Alerts: {result['alerts']}")
        if result["sepsis_prediction"] == 1:
            print("ACTION: High sepsis risk — escalating to ICU team.")
        else:
            print("STATUS: Patient stable.")
    except httpx.RequestError as e:
        print(f"ERROR: Could not reach predict function — {e}")
