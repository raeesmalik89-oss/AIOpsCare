
# AIopsCare

AIopsCare is an AI-powered IoT healthcare monitoring platform designed for real-time patient monitoring, secure access control, and machine learning–based sepsis prediction.

## Overview

The platform combines:

- IoT healthcare data ingestion
- Real-time event streaming
- Machine learning prediction services
- Authentication and authorization
- Monitoring and observability
- Containerized deployment

## Architecture

Patient Sensors
↓
Kafka Event Streaming
↓
FastAPI Backend
↓
Keycloak Authentication
↓
OPA Authorization
↓
ML Prediction Engine
↓
Prometheus Monitoring
↓
Grafana Dashboards

## Technology Stack

- Python
- FastAPI
- Docker
- Docker Compose
- PostgreSQL
- Apache Kafka
- Keycloak
- Open Policy Agent (OPA)
- Prometheus
- Grafana
- Jaeger
- OpenFaaS

## Features

- Secure JWT Authentication
- Policy-Based Authorization
- Real-Time Prediction API
- Observability & Monitoring
- Event-Driven Architecture
- Containerized Infrastructure

## Project Phases

1. Project Setup
2. Infrastructure Deployment
3. Database Integration
4. Identity & Access Management
5. Authorization Policies
6. Backend API Development
7. Event Streaming
8. AI/ML Prediction Engine
9. Monitoring & Observability
10. End-to-End Validation

## Status

Current Version: Development

Completed:
- Infrastructure Deployment
- FastAPI Backend
- Keycloak Integration
- OPA Authorization
- Prediction API
- Prometheus Monitoring

In Progress:
- Real Dataset Model Training
- Grafana Dashboards
- Jaeger Tracing
- Production Hardening

## Security Notice

This repository does not contain:
- Passwords
- API Keys
- Access Tokens
- Production Secrets
- Sensitive Patient Data

All credentials are managed through environment variables and local configuration files excluded from version control.

## Author

Raees Malik
