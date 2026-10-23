# Cloud Deployment Guide: MLOps-Driven Virtual Interior Designer

This guide details the step-by-step procedures to deploy the full-stack application (FastAPI backend + PyTorch ML classifier v003 + React/Three.js frontend + PostgreSQL database) across multiple cloud options.

---

## Architecture Overview

```
                     ┌────────────────────────────────────────┐
                     │          Cloud / Internet              │
                     └──────────────────┬─────────────────────┘
                                        │
                         HTTPS Request  │
                                        ▼
             ┌─────────────────────────────────────────────────────┐
             │       Frontend Single Page Application (SPA)        │
             │   React + Vite + Three.js + Tailwind CSS            │
             │   Hosted on Render Static Site / Vercel / Nginx     │
             └──────────────────────────┬──────────────────────────┘
                                        │ API Calls: /api/...
                                        ▼
             ┌─────────────────────────────────────────────────────┐
             │               Backend Web Service                   │
             │       FastAPI + Uvicorn (Port 8000 / $PORT)         │
             │   - MobileNetV3-Small Room Classifier (v003)       │
             │   - Algorithmic & ML Layout Recommendation Engine   │
             │   - Furniture Catalogue Service (57 Items)         │
             │   - Static Asset Serving (/static/furniture/*.svg)  │
             └──────────────────────────┬──────────────────────────┘
                                        │ SQL Queries (SQLAlchemy)
                                        ▼
             ┌─────────────────────────────────────────────────────┐
             │            Managed PostgreSQL Database              │
             │     PostgreSQL 16 (Auto-seeded on first run)        │
             └─────────────────────────────────────────────────────┘
```

---

## Option 1: Deploy with Render Blueprint (Recommended)

Render provides free/hobby-tier hosting with native PostgreSQL, Python web services, and React static sites. This repository contains a pre-configured `render.yaml` Blueprint.

### Step 1: Push Repository to GitHub or GitLab
Ensure your project is pushed to a remote GitHub or GitLab repository:
```bash
git init
git add .
git commit -m "feat: complete cloud deployment configuration"
git remote add origin https://github.com/your-username/virtual_interior_mlops.git
git push -u origin main
```

### Step 2: Create a Blueprint Instance on Render
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Blueprint**.
3. Connect your repository.
4. Render will automatically parse `render.yaml` and discover:
   - **`virtual-interior-db`**: Managed PostgreSQL 16 database.
   - **`virtual-interior-backend`**: Python 3.12 Web Service.
   - **`virtual-interior-frontend`**: Static Site with SPA routing.
5. Click **Apply**.

### Step 3: Link Frontend API Base URL
Once the backend web service is deployed, note its URL (e.g., `https://virtual-interior-backend.onrender.com`):
1. In the Render Dashboard, open **`virtual-interior-frontend`** > **Environment**.
2. Verify or update `VITE_API_BASE_URL`:
   ```
   https://virtual-interior-backend.onrender.com/api
   ```
3. Trigger a manual deploy of the frontend if the backend URL changed.

---

## Option 2: Deploy with Railway

Railway allows one-click Docker deployments with automatic environment injection.

### Step 1: Initialize Project
1. Log into [Railway.app](https://railway.app/).
2. Click **New Project** > **Deploy from GitHub repo**.
3. Select this repository.

### Step 2: Add Managed PostgreSQL
1. Inside your Railway project canvas, click **New** > **Database** > **Add PostgreSQL**.
2. Railway will generate a `DATABASE_URL` environment variable.

### Step 3: Configure Backend Service
1. Select the service created from your repo.
2. Under **Settings** > **Build**, ensure it selects `Dockerfile` at `backend/Dockerfile` (or Railway will use `railway.json`).
3. Under **Variables**, add:
   ```env
   ENVIRONMENT=production
   SQLITE_FALLBACK=false
   ACTIVE_MODEL_VERSION=v003
   FRONTEND_ORIGIN=*
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```
4. Set **Healthcheck Path** to `/api/health`.

### Step 4: Deploy Frontend Service
1. Click **New** > **GitHub Repo** > Select this repository again.
2. Under **Settings** > **Root Directory**, set `frontend`.
3. Under **Variables**, set:
   ```env
   VITE_API_BASE_URL=https://<your-backend-railway-domain>.railway.app/api
   ```
4. Railway will build and serve the frontend.

---

## Option 3: Deploy on a Linux VPS (Ubuntu / Debian with Docker)

For self-hosted virtual private servers (AWS EC2, DigitalOcean Droplet, Linode, Hetzner, etc.):

### Step 1: Install Docker & Docker Compose
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### Step 2: Clone & Configure
```bash
git clone https://github.com/your-username/virtual_interior_mlops.git
cd virtual_interior_mlops

# Create production .env file
cp .env.example .env
```
Edit `.env` and configure:
```env
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg://postgres:your_secure_password@db:5432/virtual_interior_db
SQLITE_FALLBACK=false
ACTIVE_MODEL_VERSION=v003
FRONTEND_ORIGIN=http://your-server-ip:5173,https://yourdomain.com
```

### Step 3: Build & Launch Containers
```bash
docker compose up -d --build
```

### Step 4: Verify Running Services
```bash
docker compose ps
docker compose logs -f backend
```
- Frontend will be accessible at: `http://<your-server-ip>:5173`
- Backend API Docs: `http://<your-server-ip>:8000/docs`

---

## Environment Variables Reference

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `ENVIRONMENT` | Runtime mode (`development` or `production`) | `production` |
| `PORT` | Listening port injected by cloud platform | `8000` (or dynamic cloud port) |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://user:pass@host:5432/db` |
| `SQLITE_FALLBACK` | Allow SQLite fallback if Postgres is down | `false` in production, `true` in dev |
| `ACTIVE_MODEL_VERSION` | Active ML room classification model | `v003` |
| `FRONTEND_ORIGIN` | Allowed CORS origins (comma-separated or `*`) | `https://your-frontend.onrender.com` |
| `SECRET_KEY` | App secret key for sessions | Random 32+ character string |
| `ADMIN_API_KEY` | Key for admin retraining endpoints | Random secure token |
| `VITE_API_BASE_URL` | Base URL for frontend API calls | `https://your-backend.onrender.com/api` |

---

## Post-Deployment Health Verification

After launching your deployment, execute these requests to ensure all systems are operating normally:

### 1. Backend Health Check
```bash
curl -f https://<your-backend-domain>/api/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "model_loaded": true,
  "active_version": "v003",
  "version": "1.0.0"
}
```

### 2. Verify Catalogue (57 Items)
```bash
curl -f "https://<your-backend-domain>/api/furniture?room_type=Bedroom"
```
Verifies that database seeding completed automatically and returned all matching bedroom items.

### 3. Verify ML Room Classifier
Upload a test room picture to:
```bash
curl -X POST "https://<your-backend-domain>/api/rooms/predict" \
  -F "file=@sample_room.jpg"
```
Verifies that model `v003` executes inference and returns predicted room class probabilities.
