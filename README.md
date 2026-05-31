
```bash
nano README.md
```

Replace entire content with:

```markdown
# AIOpsCare

**AI-Powered Serverless AIOps Platform for Real-Time ICU Patient Monitoring**

AIOpsCare is a production-grade, event-driven AIOps platform that performs real-time sepsis detection on ICU patient data. Built on a fully serverless, cloud-native architecture using Apache Kafka event streaming, OpenFaaS serverless functions, and a RandomForest ML model trained on real PhysioNet 2019 clinical data — with full security and observability integration.

---

## Architecture

```
PhysioNet ICU Data
        |
        v
[ Kafka Producer ] ──> [ Kafka Broker :9092 ] ──> [ Kafka Consumer ]
                        Topic: patient-vitals              |
                                                           v
                 ┌─────────────────────────────────────────────────┐
                 │              SECURITY LAYER                      │
                 │   Keycloak :8082  ──>  FastAPI :8000             │
                 │   OPA :8181       ──>  /predict /health /metrics │
                 └─────────────────────┬───────────────────────────┘
                                       │
                                       v
                 ┌─────────────────────────────────────────────────┐
                 │           SERVERLESS COMPUTE LAYER               │
                 │   OpenFaaS Gateway :8080 ──> predict-fn :5000   │
                 │   Flask handler + RandomForest ML model          │
                 │   Trained on 93,065 real ICU patient records     │
                 └─────────────────────┬───────────────────────────┘
                                       │
                                       v
                 ┌─────────────────────────────────────────────────┐
                 │            OBSERVABILITY LAYER                   │
                 │   Prometheus :9090 ──> Grafana :3000             │
                 │   OpenTelemetry :4318 ──> Jaeger :16686          │
                 └─────────────────────────────────────────────────┘
```

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

AIOpsCare uses the **PhysioNet 2019 ICU Sepsis Challenge** dataset — real anonymised clinical data from ICU patients.

| Property | Value |
|----------|-------|
| Source | PhysioNet 2019 Sepsis Challenge |
| Patient Files | 20,336 individual `.psv` files |
| Usable Records | 93,065 patient-hour records |
| Clinical Features | HR, O2Sat, Temp, SBP, MAP, Resp, Age, ICULOS |
| Target | SepsisLabel (0 = No Sepsis, 1 = Sepsis) |
| Model Accuracy | 98% on 18,613 test records |

---

## Services

| Container | Port | Role |
|-----------|------|------|
| `openfaas-gateway` | 8080 | OpenFaaS serverless gateway |
| `predict-fn` | 5000 | Sepsis prediction serverless function |
| `fastapi` | 8000 | REST API — auth, routing, validation |
| `kafka` | 9092 | Event streaming broker |
| `zookeeper` | 2181 | Kafka cluster coordination |
| `keycloak` | 8082 | JWT identity and access management |
| `opa` | 8181 | Policy-based access control |
| `postgres` | 5432 | Keycloak identity store |
| `prometheus` | 9090 | Metrics collection and alerting |
| `grafana` | 3000 | Metrics visualisation dashboards |
| `jaeger` | 16686 | Distributed request tracing |

---

## Getting Started

### Prerequisites

- Docker + Docker Compose
- Python 3.11+
- AWS EC2 (Ubuntu 26.04 LTS recommended)
- Kaggle API token

### Installation

```bash
# Clone the repository
git clone https://github.com/raeesmalik89-oss/AIOpsCare.git
cd AIOpsCare

# Create virtual environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Download PhysioNet dataset
kaggle datasets download -d salikhussaini49/prediction-of-sepsis
unzip prediction-of-sepsis.zip -d data/

# Train the ML model
python ml/train.py

# Start all services
sudo docker compose -f infrastructure/docker-compose.yml up -d
```

### Run the Streaming Pipeline

```bash
# Terminal 1 — Start Kafka consumer
python events/consumer.py

# Terminal 2 — Stream patient data
python events/producer.py
```

---

## API Reference

### Sepsis Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "HR": 125, "O2Sat": 91, "Temp": 39.2,
    "SBP": 85, "MAP": 60, "Resp": 28,
    "Age": 67, "ICULOS": 12
  }'
```

**Response:**
```json
{
  "sepsis_prediction": 1,
  "alerts": [
    "High Heart Rate Detected",
    "High Fever Detected",
    "Abnormal Respiratory Rate",
    "Low Oxygen Saturation",
    "Low Systolic Blood Pressure",
    "Low Mean Arterial Pressure"
  ]
}
```

### Get JWT Token

```bash
curl -X POST http://localhost:8082/realms/master/protocol/openid-connect/token \
  -d 'grant_type=password&client_id=admin-cli&username=admin&password=admin'
```

### OpenFaaS Function

```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{"HR":125,"O2Sat":91,"Temp":39.2,"SBP":85,"MAP":60,"Resp":28,"Age":67,"ICULOS":12}'
```

---

## Security

AIOpsCare implements a zero-trust security model:

- **Authentication** — Keycloak OpenID Connect with JWT Bearer tokens (60s expiry)
- **Authorisation** — Open Policy Agent (OPA) Rego policies on every API call
- **Vulnerability Scanning** — OWASP ZAP automated security scanning
- **Secrets Management** — All credentials via environment variables, never in code
- **Standards** — Aligned with ISO 27001, NIST Cybersecurity Framework, and GDPR

---

## Observability

- **Metrics** — Prometheus scrapes `/metrics` every 15 seconds
- **Dashboards** — Grafana visualises prediction throughput and service health
- **Tracing** — Jaeger records distributed traces for every `/predict` request
- **Instrumentation** — OpenTelemetry SDK integrated into FastAPI

---

## CI/CD

GitHub Actions pipeline runs on every push:
- Automated unit and integration tests
- Docker image build validation
- Security workflow checks

---

## Project Structure

```
AIOpsCare/
├── app/                  # FastAPI application
│   ├── main.py           # API endpoints
│   ├── auth.py           # JWT + OPA authentication
│   ├── alerts.py         # Clinical alert thresholds
│   └── schemas.py        # Pydantic data models
├── events/               # Kafka streaming
│   ├── producer.py       # PhysioNet data publisher
│   └── consumer.py       # Prediction event consumer
├── functions/predict/    # OpenFaaS serverless function
│   ├── handler.py        # ML inference handler
│   ├── entrypoint.py     # Flask HTTP wrapper
│   └── Dockerfile        # Function container
├── ml/                   # Machine learning
│   ├── train.py          # Model training pipeline
│   └── model.joblib      # Trained RandomForest model
├── infrastructure/       # Deployment
│   └── docker-compose.yml # All 11 services
├── monitoring/prometheus/ # Prometheus config
├── policies/             # OPA Rego policies
├── security/             # OWASP ZAP config
└── tests/                # Test suite
```

---

## Standards Compliance

| Standard | Coverage |
|----------|----------|
| ISO 27001 | Identity management, access control, monitoring, vulnerability management |
| NIST CSF | Identify, Protect, Detect, Respond, Recover |
| GDPR | De-identified data, minimisation, in-memory processing, research license |

---

*AIOpsCare — Designed as part of the EduQual Level 6 Diploma in AI Operations programme, demonstrating enterprise-grade serverless AIOps architecture for healthcare observability.*
```
Author

Raees Malik 
