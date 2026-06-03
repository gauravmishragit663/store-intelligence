# DESIGN.md

# Store Intelligence System Design

## Overview

This project implements an end-to-end Store Intelligence platform that transforms raw CCTV footage into actionable retail analytics. The system processes video feeds from multiple camera angles, generates structured visitor events, stores analytics data, and exposes real-time metrics through FastAPI endpoints and a live dashboard.

The primary business objective is to measure and improve offline store conversion rate by understanding customer behavior inside physical retail stores.

The system was developed using Python, YOLOv8, ByteTrack, FastAPI, SQLite, Docker, and a lightweight analytics pipeline.

---

# Architecture Overview

The system consists of four major layers:

1. Detection Layer
2. Event and Analytics Layer
3. Intelligence API Layer
4. Dashboard Layer

Raw CCTV footage enters the detection layer where customers are detected and tracked. Analytics scripts generate visitor insights such as entries, exits, zone dwell time, billing queue activity, and visitor counts. The processed information is stored in SQLite and exposed through FastAPI endpoints for reporting and dashboard consumption.

---

# Detection Layer

## Person Detection

YOLOv8 was selected as the primary object detection model for identifying people within CCTV footage.

The model processes video frames and returns bounding boxes for detected persons. Only the person class is retained while other object classes are ignored.

This approach provides:

* Fast inference speed
* Good accuracy on CCTV footage
* Simple deployment requirements
* Compatibility with CPU-only execution

---

## Visitor Tracking

ByteTrack is used for multi-object tracking.

The tracker assigns a unique tracking identifier to each detected person and maintains that identifier across consecutive frames.

Tracking enables:

* Visitor counting
* Dwell time estimation
* Entry and exit detection
* Queue duration analysis

Although tracking fragmentation occasionally occurs in crowded scenes, ByteTrack provided a practical balance between complexity and performance for the challenge dataset.

---

## Entry and Exit Analytics

Store entry cameras are processed using a virtual counting line.

Each tracked visitor is monitored relative to the counting line.

If a visitor moves from the outside region into the store region:

* ENTRY event is generated

If a visitor moves from the store region toward the outside region:

* EXIT event is generated

This logic supports visitor traffic measurement and funnel analytics.

---

## Zone Analytics

Zone cameras monitor customer activity inside product areas.

A Region of Interest (ROI) is defined around the observed shopping zone.

When a tracked visitor remains inside the ROI, dwell duration is accumulated.

Visitors exceeding the minimum dwell threshold are recorded as active zone visitors.

Metrics generated include:

* Total zone visitors
* Average dwell duration
* Most visited zone calculations

---

## Billing Queue Analytics

Billing cameras monitor customer behavior near the checkout counter.

A billing ROI is configured around the checkout area.

Tracked visitors entering the billing ROI are monitored until they leave the region.

The system calculates:

* Queue duration
* Billing area dwell time
* Billing visitor count

Store staff occasionally appear in the billing camera. ROI restrictions and dwell thresholds are used to reduce staff-related false positives.

---

# Event and Analytics Layer

Analytics results are persisted in SQLite.

The database stores:

* Visitor identifiers
* Zone names
* Dwell duration
* Camera identifiers
* Visit timestamps

This storage layer enables historical reporting and API-based metric aggregation.

The event schema was intentionally simplified compared to a production event streaming architecture to reduce implementation complexity while maintaining compatibility with required analytics queries.

---

# Intelligence API Layer

FastAPI is used to expose analytics endpoints.

Implemented endpoints include:

* /events/ingest
* /events
* /metrics
* /stores/{id}/metrics
* /funnel
* /heatmap
* /anomalies
* /dashboard-summary
* /sales-summary
* /top-zone
* /health

The API performs:

* Event ingestion
* Metric aggregation
* Visitor funnel reporting
* Zone performance reporting
* Sales analytics
* Operational monitoring

The API is containerized and can be executed using Docker.

---

# Dashboard Layer

A lightweight dashboard consumes API responses and presents operational metrics.

Dashboard functionality includes:

* Visitor counts
* Average dwell time
* Zone popularity
* Sales summaries
* Conversion-related metrics

The dashboard provides a near real-time view of store activity using the analytics generated from CCTV processing.

---

# Production Readiness

Several production-oriented practices were incorporated into the implementation:

## Structured Logging

Request metadata including endpoint information, response status, and execution details are logged using structured logging configuration.

## Testing

Pytest-based tests validate:

* Event ingestion
* Dashboard responses
* Sales endpoints
* Zone analytics endpoints

Prompt blocks were included in test files to document AI-assisted test generation as required by the challenge.

## Docker Support

Docker configuration enables reproducible deployment and simplified execution on clean environments.

## Database Persistence

SQLite provides lightweight persistence without requiring additional infrastructure.

For larger-scale deployments, PostgreSQL would be a more appropriate production database.

---

# AI-Assisted Decisions

AI tools were used throughout development to accelerate implementation and evaluate architectural trade-offs.

### Decision 1: Detection and Tracking Approach

AI suggested multiple alternatives including YOLOv8 + DeepSORT, YOLOv8 + ByteTrack, and RT-DETR-based solutions.

After evaluating complexity and implementation effort, YOLOv8 with ByteTrack was selected because it provided sufficient accuracy while remaining easy to deploy and debug.

### Decision 2: Database Architecture

AI recommended both PostgreSQL and SQLite approaches.

SQLite was selected because the challenge dataset is relatively small, deployment simplicity was important, and container setup becomes significantly easier.

### Decision 3: Store 2 Adaptation Strategy

AI suggested creating store-specific analytics pipelines rather than forcing a single generalized configuration.

This recommendation was adopted because Store 2 camera layouts differ from Store 1 layouts, particularly for entry counting, billing ROI placement, and zone coverage.

The resulting implementation produced more accurate visitor analytics while keeping the pipeline easy to understand.

---

# Limitations and Future Improvements

Several enhancements would be implemented for a production-scale deployment:

* Cross-camera re-identification
* Staff classification using appearance models
* Event streaming via Kafka
* PostgreSQL storage
* Real-time WebSocket analytics
* Advanced anomaly detection
* Multi-store distributed processing
* Queue abandonment prediction
* Customer journey reconstruction across cameras

Despite these limitations, the implemented system successfully demonstrates the complete pipeline from raw CCTV footage to actionable retail intelligence.
-------------------------------------------------------------------