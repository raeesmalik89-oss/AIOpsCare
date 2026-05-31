
import os
import json
import time
import glob
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
DATA_PATH = "data/training_setA/training"
TOPIC = "patient-vitals"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def stream_patients():
    files = sorted(glob.glob(f"{DATA_PATH}/*.psv"))[:50]
    print(f"Streaming {len(files)} patient files to Kafka topic: {TOPIC}")
    for filepath in files:
        patient_id = os.path.basename(filepath).replace(".psv", "")
        with open(filepath) as f:
            headers = f.readline().strip().split("|")
            for line in f:
                values = line.strip().split("|")
                record = dict(zip(headers, values))
                record["patient_id"] = patient_id
                producer.send(TOPIC, value=record)
                print(f"Sent: {patient_id} -> HR={record.get('HR','N/A')}")
                time.sleep(0.1)
    producer.flush()
    print("Streaming complete.")

if __name__ == "__main__":
    stream_patients()
