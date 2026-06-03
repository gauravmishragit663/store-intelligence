

# Store Intelligence System

## Overview

This project implements an AI-powered Store Intelligence System that transforms CCTV footage and POS transaction data into actionable retail analytics.

The solution processes multiple camera feeds, tracks visitors, measures dwell times, analyzes customer movement patterns, detects billing queue behavior, and exposes business metrics through FastAPI endpoints and a lightweight dashboard.

The system was developed as part of the Purplle Tech Challenge.

---

## Key Features

### Visitor Analytics

* Visitor detection using YOLOv8
* Multi-person tracking using ByteTrack
* Visitor counting
* Visitor persistence across frames

### Entry / Exit Analytics

* Store entry counting
* Store exit counting
* Line crossing based tracking
* Visitor flow analysis

### Zone Analytics

* ROI-based zone monitoring
* Dwell time measurement
* Zone popularity tracking
* Top zone identification

### Billing Queue Analytics

* Billing area monitoring
* Queue dwell time estimation
* Queue visitor counting
* Billing congestion insights

### Sales Analytics

* POS transaction processing
* Revenue aggregation
* Order statistics
* Brand performance analysis

### Dashboard APIs

* Dashboard summary
* Sales summary
* Top zone analytics
* Metrics APIs
* Funnel analytics
* Heatmap analytics
* Anomaly detection APIs

---

## System Architecture

CCTV Cameras
↓
YOLOv8 Detection
↓
ByteTrack Tracking
↓
Analytics Engine
↓
SQLite Storage
↓
FastAPI Services
↓
Dashboard

---

## Technology Stack

### Computer Vision

* YOLOv8
* OpenCV
* Supervision
* ByteTrack

### Backend

* FastAPI
* Pydantic
* SQLAlchemy

### Database

* SQLite

### Dashboard

* HTML
* JavaScript

### Deployment

* Docker
* Docker Compose

### Testing

* Pytest

---

## Project Structure

app/

* FastAPI services
* Database models
* API endpoints

pipeline/

* CCTV analytics pipelines
* Entry/Exit tracking
* Zone analytics
* Billing analytics
* Dwell time analytics

dashboard/

* Frontend dashboard

data/

* POS transaction dataset

docs/

* DESIGN.md
* CHOICES.md

tests/

* API validation tests

---

## Analytics Implemented

### Store 1

* Entry Analytics
* Zone Analytics
* Billing Analytics

### Store 2

* Entry Analytics
* Exit Analytics
* Zone Analytics
* Billing Analytics

---

## API Endpoints

### Event APIs

* POST /events/ingest
* GET /events

### Metrics APIs

* GET /metrics
* GET /stores/{store_id}/metrics

### Analytics APIs

* GET /funnel
* GET /heatmap
* GET /anomalies

### Dashboard APIs

* GET /dashboard-summary
* GET /sales-summary
* GET /top-zone

---

## Testing

Pytest-based test suite validates:

* Event ingestion
* Duplicate handling
* Metrics APIs
* Funnel APIs
* Heatmap APIs
* Dashboard APIs
* Sales APIs
* Zone APIs

Current coverage is approximately 90%+.

---

## Docker Execution

Build:

docker compose build

Run:

docker compose up

API:

[http://localhost:8000](http://localhost:8000)

Dashboard:

[http://localhost:8000/dashboard](http://localhost:8000/dashboard)

---

## Design Decisions

Key engineering decisions are documented in:

* docs/DESIGN.md
* docs/CHOICES.md

---

## Limitations

* Cross-camera re-identification is not implemented.
* Staff identification is rule-based.
* SQLite is used for challenge simplicity.
* Queue estimation depends on camera placement and ROI quality.

---

## Future Enhancements

* Cross-camera visitor re-identification
* PostgreSQL migration
* Kafka streaming pipeline
* Real-time dashboard updates
* Advanced anomaly detection
* Customer journey reconstruction

---

## Conclusion

The implemented solution successfully demonstrates an end-to-end retail intelligence platform capable of converting raw CCTV footage and POS data into measurable business insights. The system combines computer vision, analytics, APIs, persistence, testing, and deployment capabilities in a production-inspired architecture suitable for further extension.

