
# -----------------------------------
# Kafka Event Streaming Tests
# -----------------------------------

from kafka import KafkaProducer
import json


# -----------------------------------
# Test Kafka Producer Creation
# -----------------------------------

def test_kafka_producer_creation():

    producer = KafkaProducer(
        bootstrap_servers='kafka:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    assert producer is not None


# -----------------------------------
# Test Event Serialization
# -----------------------------------

def test_event_serialization():

    patient_event = {
        "heart_rate": 120,
        "temperature": 39.5,
        "respiratory_rate": 30
    }

    serialized = json.dumps(patient_event)

    assert isinstance(serialized, str)


# -----------------------------------
# Test Kafka Topic Send
# -----------------------------------

def test_kafka_send():

    producer = KafkaProducer(
        bootstrap_servers='kafka:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    patient_event = {
        "heart_rate": 120,
        "temperature": 39.5,
        "respiratory_rate": 30
    }

    future = producer.send(
        "patient-events",
        patient_event
    )

    producer.flush()

    assert future is not None
