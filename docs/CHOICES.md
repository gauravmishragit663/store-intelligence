# Engineering Choices

## Problem Understanding

Goal:
Convert raw CCTV footage and POS transactions into actionable store intelligence.

Required outputs:

- Visitor counting
- Entry / Exit tracking
- Dwell time analytics
- Billing queue analytics
- Zone analytics
- Store KPIs
- Dashboard APIs

---

## Choice 1: YOLOv8 for Person Detection

### Alternatives Considered

- Faster R-CNN
- SSD
- YOLOv5
- YOLOv8

### Decision

YOLOv8n selected.

### Reason

- Fast inference
- Easy integration
- Good accuracy
- Lightweight for local execution

### Tradeoff

Slightly lower accuracy than larger models but much faster.

---

## Choice 2: ByteTrack for Tracking

### Alternatives Considered

- DeepSORT
- SORT
- ByteTrack

### Decision

ByteTrack selected.

### Reason

- Simple integration
- Strong ID persistence
- Works well in crowded retail scenes

### Tradeoff

Cross-camera re-identification not supported.

---

## Choice 3: SQLite Storage

### Alternatives Considered

- PostgreSQL
- MongoDB
- SQLite

### Decision

SQLite selected.

### Reason

- Zero setup
- Lightweight
- Ideal for challenge scope

### Tradeoff

Not suitable for large-scale production deployments.

---

## Choice 4: FastAPI

### Alternatives Considered

- Flask
- Django
- FastAPI

### Decision

FastAPI selected.

### Reason

- Automatic OpenAPI docs
- Type validation
- High performance

### Tradeoff

Smaller ecosystem than Django.

---

## Choice 5: Rule-Based Analytics

### Decision

Used ROI + tracking based analytics.

### Reason

- Transparent logic
- Easy debugging
- Reproducible results

### Tradeoff

Less adaptive than learned behavior models.

---

## Choice 6: Multi-Camera Processing

### Decision

Process each camera independently.

### Reason

- Simpler implementation
- Reduced complexity
- Reliable within challenge timeline

### Tradeoff

No cross-camera identity matching.

---

## AI Assistance Disclosure

AI tools were used for:

- Architecture brainstorming
- Code reviews
- Documentation drafting

Final implementation, debugging, validation, testing, ROI tuning, analytics logic and integration decisions were performed manually.