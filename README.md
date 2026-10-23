# MLOps-Driven Virtual Interior Designer Using AR

An end-to-end intelligent interior design platform that integrates deep learning room classification, deterministic explainable layout recommendations, interactive 3D web manipulation, and a closed-loop MLOps retraining lifecycle.

---

## 1. Project Overview & Architecture

### The System Workflow
1. **Transfer Learning Vision Classifier:** Powered by PyTorch and MobileNetV3-Small to identify room typology (`Bedroom`, `LivingRoom`, `Kitchen`, `DiningRoom`, `Bathroom`, `HomeOffice`, `Other`).
2. **Deterministic Layout Recommendation Engine:** Applies interior design heuristics and spatial clearance bounding boxes to place appropriate furniture items with mathematical reproducibility and collision avoidance.
3. **Interactive 3D Web Studio:** Developed with Three.js and React Three Fiber, rendering room dimensions, directional lighting, and procedural furniture geometry with real-time translation, rotation, and top-down floor-plan views.
4. **Governed MLOps Pipeline:** Captures user ratings and ground-truth corrections, logs prediction latency, enforces evaluation thresholds, and supports candidate model training and zero-downtime model promotion.

```mermaid
flowchart TD
    subgraph Client ["Client Browser (React 18 + Three.js)"]
        UI[Upload Room Photo] --> Analysis[Room Classification View]
        Analysis --> Designer[3D Room Studio]
        Designer --> Feedback[User Feedback & Layout Adjustments]
        MLOpsUI[MLOps Telemetry Dashboard]
    end

    subgraph Backend ["Backend API (FastAPI)"]
        API[API Gateway & Router]
        ImageSvc[Image Validation & Storage]
        InfSvc[Inference Service / Model Cache]
        LayoutEng[Deterministic Layout Engine]
        FeedSvc[Feedback Aggregator]
        RetrainSvc[Retraining & Promotion Worker]
    end

    subgraph Storage ["Database & Storage"]
        DB[(PostgreSQL / SQLite Dev)]
        Disk[Local Uploads & ML Artifacts]
    end

    subgraph ML ["Machine Learning Pipeline"]
        Model[MobileNetV3-Small Classifier]
        Eval[Evaluator - Accuracy, Macro F1, Confusion Matrix]
        Registry[Model Checkpoint Registry]
    end

    UI -->|multipart/form-data| API
    API --> ImageSvc --> Disk
    API --> InfSvc --> Model
    InfSvc -->|Log Event| DB
    Analysis --> LayoutEng --> DB
    Designer -->|Save Layout| DB
    Feedback -->|Submit Feedback| FeedSvc --> DB
    MLOpsUI -->|Status & Metrics| API
    MLOpsUI -->|Trigger Retraining| RetrainSvc
    RetrainSvc --> Eval --> Registry --> InfSvc
```

---

## 2. Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, React Three Fiber (`@react-three/fiber`), Three.js, Drei (`@react-three/drei`), TanStack Query, React Router v6, Lucide React.
- **Backend API:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, psycopg 3, Pillow, OpenCV, python-multipart.
- **Machine Learning & MLOps:** PyTorch, torchvision, MobileNetV3-Small transfer learning, scikit-learn, NumPy, MLflow.
- **Database:** PostgreSQL 16 (with isolated SQLite development mode).
- **Testing:** pytest (25 backend and ML tests), Vitest (2 frontend component tests).
- **Infrastructure:** Docker, Docker Compose, structured logging with masked credentials.

---

## 3. Database Architecture & Configuration

The application uses SQLAlchemy 2.0 with 12 relational models:
- `users`: User profiles and preferences.
- `rooms`: Room dimensions ($W \times L \times H$), style, and budget preferences.
- `room_predictions`: Vision model inference output, confidence, top-3 candidates, latency.
- `furniture_items`: 3D furniture catalog with bounding boxes and clearance envelopes.
- `layouts`: Room layout configurations.
- `layout_items`: Positioned furniture items with Cartesian $(X, Y, Z)$ coordinates and rotation angles.
- `user_feedback`: User ratings, dissatisfaction reasons, manual layout adjustments, and room type corrections.
- `training_jobs`: Retraining jobs tracking (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`).
- `model_versions`: Registered model checkpoints with accuracy, macro F1, and promotion flags.
- `model_evaluations`: Evaluated metrics on held-out test splits.
- `experiment_runs`: MLflow parameters and metrics tracking.
- `prediction_events`: Real-time inference latency logs.

### Database Connection Behavior:
1. `DATABASE_URL` is read from environment configuration (`.env`).
2. Log messages always mask database passwords (e.g. `postgresql+psycopg://postgres:***@localhost:5432/virtual_interior_db`).
3. If PostgreSQL is offline during development and `SQLITE_FALLBACK=true`, the app activates local SQLite (`virtual_interior_dev.db`) and transparently reports `"status": "degraded"`, `"active_database_backend": "sqlite_fallback"`, `"is_sqlite_fallback": true` in `GET /api/health/ready`.
4. In production (`ENVIRONMENT=production` or `SQLITE_FALLBACK=false`), the application strictly refuses silent fallback and throws a `RuntimeError` if PostgreSQL cannot be reached.

---

## 4. Quick Start & Execution

### Option A: Docker Compose (Full Stack)
```bash
# Start PostgreSQL, FastAPI backend, and React frontend
docker compose up --build -d

# Check service logs
docker compose logs -f backend
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`
- Readiness check: `http://localhost:8000/api/health/ready`

### Option B: Local Development (Windows PowerShell)

#### 1. Backend Setup (PowerShell)
```powershell
# 1. Activate or create virtual environment (recommended)
# python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install -r backend/requirements.txt

# 3. Verify .env file exists (or copy from .env.example)
if (-not (Test-Path .env)) { Copy-Item .env.example .env }

# 4. Generate architectural SVG furniture assets (if needed)
python scripts/generate_furniture_assets.py

# 5. Start the backend server on port 8000
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Swagger UI Documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`
- Readiness check: `http://localhost:8000/api/health/ready`
- Furniture Catalog API: `http://localhost:8000/api/furniture`
- Room Prediction API: `http://localhost:8000/api/v1/rooms/predict`

#### 2. Frontend Setup (PowerShell)
```powershell
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Start Vite development server on port 5173
npm run dev
```
- Application Web UI: `http://localhost:5173`
- Furniture Catalog: `http://localhost:5173/catalog`
- Room Upload & Vision Analysis: `http://localhost:5173/upload`
- 3D Room Designer Studio: `http://localhost:5173/designer`
- MLOps Telemetry Hub: `http://localhost:5173/mlops`

---

## 5. Furniture Catalogue & Asset Serving Strategy

### Root Cause Diagnosis & Solution
- **Prior Issue:** Catalogue seed records lacked `image_url` fields and the FastAPI backend had no static mount for static furniture assets, causing furniture cards to show no images.
- **Image Strategy:**
  1. **Architectural Vector Illustrations:** 18 bespoke, category-specific SVG vector illustrations (`sofa_nordic_3seater.svg`, `bed_platform_queen.svg`, etc.) matching each furniture item's category, style, and metric dimensions.
  2. **Static Asset Mount:** Mounted in FastAPI at `/static` (`backend/app/static/furniture/`) and mirrored in `frontend/public/furniture/` and `frontend/public/static/furniture/`.
  3. **Vite Proxy & Resolution:** `vite.config.ts` proxies `/static`, `/uploads`, and `/api` to `http://localhost:8000`. `frontend/src/utils/image.ts` (`resolveImageUrl`) safely resolves asset paths.
  4. **Multi-Mode Rendering & Fallbacks:** Every furniture card renders the item's image with `aspect-[4/3]`, `object-contain`, smooth loading shimmer (`animate-pulse`), and includes an interactive 3D/Photo toggle button. If an image fails to load, it falls back immediately to procedural Three.js 3D geometry without retry loops.
  5. **Idempotent Seeding:** `FurnitureService.seed_catalog()` updates existing records with missing `image_url` and inserts new items idempotently without resetting the database.

---

## 5. Machine Learning & Retraining Pipeline

### Room Classification Model
- **Architecture:** MobileNetV3-Small with custom classification head.
- **Classes (7):** `Bedroom`, `LivingRoom`, `Kitchen`, `DiningRoom`, `Bathroom`, `HomeOffice`, `Other`.
- **Inference Preprocessing:** Resize to $224 \times 224$, Normalize with ImageNet mean `[0.485, 0.456, 0.406]` and std `[0.229, 0.224, 0.225]`.

### Model v003 Integration & Room Typology Classification
The application integrates trained MobileNetV3-Small model **`v003`** trained on real Kaggle House Rooms images with **84.45% test accuracy** and **0.8447 macro F1** across 1,003 test samples.

#### Active Model Configuration
- **Active Model Version:** `v003` (configurable via `ACTIVE_MODEL_VERSION` in `.env`)
- **Weights File:** `ml/artifacts/model_v003.pth`
- **Metadata File:** `ml/artifacts/model_v003.json`
- **Architecture:** `MobileNetV3-Small` transfer learning head with dropout
- **Output Classes (6):** `Bathroom`, `Bedroom`, `DiningRoom`, `HomeOffice`, `Kitchen`, `LivingRoom`
- **Inference Hardware:** CPU optimized (`map_location="cpu"`, `torch.inference_mode()`)

#### Room Prediction API Endpoint
- **URL:** `POST /api/v1/rooms/predict` (also available as `POST /api/rooms/predict`)
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file`: Uploaded photograph (`image/jpeg`, `image/png`, `image/webp`, max 10MB)

##### Example `curl` Request:
```bash
curl -X POST "http://localhost:8000/api/v1/rooms/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@ml/data/processed/house_rooms/test/Bedroom/bedroom_00000.jpg"
```

##### Response Schema:
```json
{
  "model_version": "v003",
  "predicted_room": "Bedroom",
  "confidence": 0.999,
  "probabilities": {
    "Bathroom": 0.0,
    "Bedroom": 0.999,
    "DiningRoom": 0.0001,
    "HomeOffice": 0.0,
    "Kitchen": 0.0,
    "LivingRoom": 0.001
  },
  "latency_ms": 14.2,
  "is_demo_fallback": false
}
```

#### Model Status Endpoint
- **URL:** `GET /api/v1/rooms/model-status` (and `GET /api/rooms/model-status`)
- **Response:**
```json
{
  "model_version": "v003",
  "is_loaded": true,
  "is_trained": true,
  "device": "cpu",
  "architecture": "MobileNetV3-Small",
  "classes": ["Bedroom", "LivingRoom", "Kitchen", "DiningRoom", "Bathroom", "HomeOffice"],
  "num_classes": 6
}
```

#### Interactive Swagger UI Testing
1. Start the backend: `python -m uvicorn backend.app.main:app --port 8000 --reload`
2. Open Swagger UI at: `http://localhost:8000/docs`
3. Expand **Rooms** $\rightarrow$ `POST /api/v1/rooms/predict`
4. Click **Try it out**, upload a room photo, and click **Execute**.

---

### Governed Feedback Retraining Loop
1. When users upload room photos, predictions are recorded in `room_predictions`.
2. If users submit a correction (e.g. classified as `DiningRoom` but corrected to `LivingRoom`), this is stored in `user_feedback`.
3. An administrator verifies and approves corrections via `POST /api/feedback/{feedback_id}/approve`.
4. When `POST /api/mlops/train` is triggered:
   - **Pre-check:** If approved feedback samples are below the configured minimum (`MIN_APPROVED_FEEDBACK_SAMPLES=10`), the request is immediately rejected with **HTTP 400 Bad Request** before any training job is queued.
   - **Concurrency Check:** If another training job is currently active, returns **HTTP 409 Conflict**.
   - **Candidate Isolation:** The new model is trained as a separate candidate (`is_active=False`).
   - **Held-Out Evaluation:** Evaluated on held-out test splits without data leakage.
   - **Quality Gate:** If accuracy does not satisfy configured quality gates (`>= 0.50`), promotion is blocked.
   - **Promotion:** When `POST /api/mlops/promote/{version_tag}` is called on an eligible candidate that passed quality gates, it is promoted to production and inference cache is atomically hot-reloaded.

---

## 6. Verification & Test Suite

### Run All Backend and ML Tests (pytest):
```powershell
python -m pytest ml/tests backend/tests -v
```
**Results:** **57 passed, 0 failed in ~59.7s**
- `backend/tests/test_furniture.py`: 7 passed (catalog retrieval, image_url presence, static asset resolution via FastAPI, room_type filtering, category filter, price filter, 404 handling)
- `backend/tests/test_room_inference.py`: 9 passed (v003 loading, architecture, class ordering, CPU inference, endpoints, validations, corrupt files, oversized uploads, model status)
- `ml/tests/test_dataset_loaders.py`: 7 passed (split loading, 6,610 counts, no cross-split leakage, consistency, validations)
- `ml/tests/test_dataset_preparation.py`: 5 passed (label mapping, near-duplicate clustering, exclusions, corrupted images)
- `ml/tests/test_layout_ml.py`: 7 passed (bounding box containment, candidate scoring, synthetic dataset)
- `ml/tests/test_ml_pipeline.py`: 3 passed (architecture, transform shapes, metric computation)
- `backend/tests/test_end_to_end_flow.py`: 1 passed (full virtual interior workflow)
- `backend/tests/test_feedback.py`: 1 passed
- `backend/tests/test_health.py`: 2 passed (liveness and readiness)
- `backend/tests/test_layouts.py`: 3 passed (recommendation, collision warnings, custom layout)
- `backend/tests/test_mlops.py`: 9 passed (MLOps status, metrics, quality gates, candidate promotion)
- `backend/tests/test_rooms.py`: 3 passed (analysis, MIME validation, room retrieval)

### Run Frontend Component Tests (Vitest):
```bash
cd frontend
npm test -- --run
```
**Results:** **2 passed in 1.65s**

### Run Frontend Type Check & Build:
```bash
cd frontend
npm run build
```
**Results:** `tsc && vite build` built cleanly (2132 modules transformed into `dist/` with 0 errors).

---

## 7. WebXR and Device Limitations

The application provides an interactive **3D Web Studio** directly inside any desktop or mobile browser via WebGL and Three.js. This includes:
- Metric room boundary modeling.
- Real-time 3D translation along $(X, Z)$ ground planes.
- Real-time Y-axis rotation.
- Top-down 2D floor-plan toggle.
- Clearance collision prevention.

**Camera-Based AR Distinction:**
True surface-scanning Augmented Reality (projecting digital furniture onto physical room floors through live camera pass-through) requires hardware SLAM / depth sensors supported by ARCore (Android) or ARKit (iOS). The frontend includes a WebXR session detector modal that notifies users when opening the app on devices without hardware WebXR AR support.
