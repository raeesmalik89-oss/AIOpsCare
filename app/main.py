
import os

from fastapi import FastAPI, Depends

from app.schemas import PatientData
from app.model_loader import model
from app.alerts import generate_alerts
from app.auth import authorize

from prometheus_fastapi_instrumentator import Instrumentator

# -----------------------------------
# OpenTelemetry Imports
# -----------------------------------

from opentelemetry import trace

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter
)

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)


# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI(
    title="AIOpsCare",
    description="Real-Time ICU Monitoring & Sepsis Prediction Platform",
    version="1.0.0",
)


# -----------------------------------
# Prometheus Metrics
# -----------------------------------

Instrumentator().instrument(app).expose(app)


# -----------------------------------
# OpenTelemetry Configuration
# -----------------------------------

resource = Resource.create({
    "service.name": "aiopscare-fastapi"
})

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer = trace.get_tracer(__name__)


# -----------------------------------
# OTLP Exporter
# -----------------------------------

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True
)

span_processor = BatchSpanProcessor(
    otlp_exporter
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)


# -----------------------------------
# FastAPI Instrumentation
# -----------------------------------

FastAPIInstrumentor.instrument_app(app)


# -----------------------------------
# API Routes
# -----------------------------------

@app.get("/")
async def root():
    return {
        "message": "AIOpsCare API running successfully"
    }


@app.post("/predict")
async def predict(
    data: PatientData,
    token: str = Depends(authorize)
):

    with tracer.start_as_current_span(
        "predict-sepsis"
    ):

        prediction = model.predict([[
            data.heart_rate,
            data.temperature,
            data.respiratory_rate,
        ]])

        result = int(prediction[0])

        alerts = generate_alerts(data)

        return {
            "sepsis_prediction": result,
            "alerts": alerts
        }
