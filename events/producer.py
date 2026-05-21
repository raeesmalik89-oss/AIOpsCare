

# -----------------------------------
# Kafka ICU Event Producer
# -----------------------------------

from kafka import KafkaProducer
import json

# Kafka Producer Configuration

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send ICU Patient Event

patient_event = {
    "heart_rate": 120,
    "temperature": 39.2,
    "respiratory_rate": 30
}

producer.send("patient-events", patient_event)

producer.flush()

print("Patient event sent successfully.")
