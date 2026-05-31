
# AIOpsCare

**AI-Powered Serverless AIOps Platform for Real-Time ICU Patient Monitoring**

AIOpsCare is a production-grade, event-driven AIOps platform that performs real-time sepsis detection on ICU patient data. Built on a fully serverless, cloud-native architecture using Apache Kafka event streaming, OpenFaaS serverless functions, and a RandomForest ML model trained on real PhysioNet 2019 clinical data.

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Serverless Platform | OpenFaaS | Gateway v0.27.13 |
| Event Streaming | Apache Kafka + Zookeeper | Confluent 7.4.0 |
| API Framework | FastAPI + Uvicorn | 0.136.1 |
| ML Engine | Scikit-learn RandomForestClassifier | 1.8.0 |
| Identity Provider | Keycloak | 24.0.3 |
| Policy Engine | Open Policy Agent | Latest |
| Security Scanning | OWASP ZAP | Latest |
| Metrics | Prometheus | Latest |
| Dashboards | Grafana | 13.0.1 |
| Tracing | Jaeger + OpenTelemetry | Latest |
| Database | PostgreSQL | 15 |
| Cloud | AWS EC2 Ubuntu 26.04 LTS | 30GB EBS |

---

## Dataset

| Property | Value |
|----------|-------|
| Source | PhysioNet 2019 ICU Sepsis Challenge |
| Patient Files | 20,336 individual .psv files |
| Usable Records | 93,065 patient-hour records |
| Clinical Features | HR, O2Sat, Temp, SBP, MAP, Resp, Age, ICULOS |
| Target | SepsisLabel (0 = No Sepsis, 1 = Sepsis) |
| Model Accuracy | 98% on 18,613 test records |

---

## Services

| Container | Port | Role |
|-----------|------|------|
| openfaas-gateway | 8080 | OpenFaaS serverless gateway |
| predict-fn | 5000 | Sepsis prediction serverless function |
| fastapi | 8000 | REST API - auth, routing, validation |
| kafka | 9092 | Event streaming broker |
| zookeeper | 2181 | Kafka cluster coordination |
| keycloak | 8082 | JWT identity and access management |
| opa | 8181 | Policy-based access control |
| postgres | 5432 | Keycloak identity store |
| prometheus | 9090 | Metrics collection and alerting |
| grafana | 3000 | Metrics visualisation dashboards |
| jaeger | 16686 | Distributed request tracing |

---

## Getting Started

### Prerequisites

- Docker + Docker Compose
- Python 3.11+
- AWS EC2 Ubuntu 26.04 LTS
- Kaggle API token

### Installation

    git clone https://github.com/raeesmalik89-oss/AIOpsCare.git
    cd AIOpsCare
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    kaggle datasets download -d salikhussaini49/prediction-of-sepsis
    python ml/train.py
    sudo docker compose -f infrastructure/docker-compose.yml up -d

### Run Streaming Pipeline

    source venv/bin/activate
    python events/consumer.py   # Terminal 1
    python events/producer.py   # Terminal 2

---

## API Reference

### Sepsis Prediction

    curl -X POST http://localhost:8000/predict
      -H "Authorization: Bearer <jwt-token>"
      -H "Content-Type: application/json"
      -d '{"HR":125,"O2Sat":91,"Temp":39.2,"SBP":85,"MAP":60,"Resp":28,"Age":67,"ICULOS":12}'

### Get JWT Token

    curl -X POST http://localhost:8082/realms/master/protocol/openid-connect/token
      -d "grant_type=password&client_id=admin-cli&username=admin&password=admin"

### OpenFaaS Direct

    curl -X POST http://localhost:5000/
      -H "Content-Type: application/json"
      -d '{"HR":125,"O2Sat":91,"Temp":39.2,"SBP":85,"MAP":60,"Resp":28,"Age":67,"ICULOS":12}'

---

## Project Structure

    AIOpsCare/
    app/                    FastAPI application
    events/                 Kafka producer and consumer
    functions/predict/      OpenFaaS serverless function
    ml/                     Model training and inference
    infrastructure/         Docker Compose - all 11 services
    monitoring/prometheus/  Prometheus configuration
    policies/               OPA Rego policies
    security/               OWASP ZAP configuration
    tests/                  Test suite

---

## Security

- Authentication - Keycloak OpenID Connect with JWT Bearer tokens
- Authorisation - Open Policy Agent Rego policies on every API call
- Vulnerability Scanning - OWASP ZAP automated security scanning
- Secrets Management - All credentials via environment variables
- Standards - ISO 27001, NIST Cybersecurity Framework, GDPR compliant

---

## Observability

- Metrics - Prometheus scrapes /metrics every 15 seconds
- Dashboards - Grafana visualises prediction throughput and service health
- Tracing - Jaeger records distributed traces for every /predict request
- Instrumentation - OpenTelemetry SDK integrated into FastAPI

---

*AIOpsCare - EduQual Level 6 Diploma in AI Operations | Serverless AIOps Architecture for Healthcare Observability*
