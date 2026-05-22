# CIPHER — CI/CD Intelligent Pipeline Health Engine with Autonomous Retraining
<img width="1314" height="585" alt="image" src="https://github.com/user-attachments/assets/6d6f2113-8b1d-4912-8d27-a7bfaed428d2" />







> An AI-powered DevOps SaaS that automatically analyzes CI/CD pipeline failures and posts plain-English root cause + fix suggestions as GitHub PR comments — within 30 seconds.
---

## The Problem

Every developer wastes 15–45 minutes per day reading CI/CD logs, Googling errors, and manually copying logs into ChatGPT. CIPHER eliminates this entirely.

## How it Works
Pipeline fails → GitHub webhook → CIPHER analyzes log → PR comment posted in 30s

↓

Engineer rates 👍/👎

↓

Weekly model retraining
↓
Model gets smarter automatically

---

## Architecture

> View the interactive architecture: [cipher-architecture.html](./docs/cipher-architecture.html)
┌─────────────────────────────────────────────────────────┐
│                    AWS Infrastructure                    │
│  EC2 (k3s) · RDS PostgreSQL · ElastiCache · S3 · ECR   │
└─────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────┐
│                   Kubernetes (k3s)                      │
│                                                         │
│  GitHub ──► Webhook ──► Kafka ──► Analysis              │
│                                      │                  │
│                              Inference (AI) ◄── MLflow  │
│                                      │                  │
│                           Notification ──► PR Comment   │
│                                      │                  │
│                            Feedback ──► Retraining      │
└─────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────┐
│              Observability (Prometheus + Grafana)        │
└─────────────────────────────────────────────────────────┘
---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI (5 microservices) |
| Frontend | Next.js 14, React, Tailwind CSS |
| AI/ML | TF-IDF + LogReg → DistilBERT, MLflow registry |
| Messaging | Apache Kafka |
| Database | PostgreSQL (SQLAlchemy async) |
| Cache | Redis |
| Container | Docker, Docker Compose |
| Orchestration | Kubernetes (k3s) with HPA autoscaling |
| IaC | Terraform (VPC, RDS, ElastiCache, S3, ECR) |
| CI/CD | GitHub Actions (build + test + deploy) |
| Monitoring | Prometheus + Grafana |
| Billing | Stripe (Free / $29 / $99 plans) |

---

## Microservices

| Service | Port | Responsibility |
|---------|------|---------------|
| auth-service | 8001 | JWT auth, user management, Stripe billing |
| webhook-service | 8002 | GitHub webhook receiver, HMAC validation |
| analysis-service | 8003 | Log parser, GitHub API, Kafka consumer |
| inference-service | 8004 | AI classification, MLflow model loading |
| notification-service | 8005 | PR commenter, feedback collection |
| frontend | 3000 | Next.js SaaS dashboard |
| mlflow | 5000 | Model registry, experiment tracking |

---

## AI Pipeline — 3 Stages of Intelligence

| Stage | When | Method | Accuracy |
|-------|------|--------|----------|
| 1 — Rule-based | Day 0 | 20 regex patterns, 6 categories | ~68% |
| 2 — LLM | Week 2+ | AWS Bedrock structured prompt | ~88% |
| 3 — Fine-tuned | Month 2+ | DistilBERT trained on real data | ~93% |

The model **self-improves every Sunday** — engineer feedback becomes labeled training data, the model retrains on SageMaker, and only promotes to Production if F1 score improves by >2%.

---

## Failure Categories

CIPHER classifies pipeline failures into 6 categories:

| Category | Example |
|----------|---------|
| `test_failure` | `FAILED tests/test_auth.py - AssertionError` |
| `dependency_error` | `ModuleNotFoundError: No module named requests` |
| `build_error` | `SyntaxError: invalid syntax line 42` |
| `auth_failure` | `Permission denied: credentials invalid` |
| `infra_error` | `Connection refused: dial tcp :5432` |
| `timeout` | `Job exceeded maximum time limit` |

---

## Quick Start

```bash
git clone https://github.com/ansh9197/Cipher.git
cd Cipher
./scripts/start-all.sh
```

---

## Live Demo

| URL | What you see |
|-----|-------------|
| http://13.232.125.216:3000 | Product — register and explore dashboard |
| http://13.232.125.216:8001/docs | Auth API — interactive Swagger docs |
| http://13.232.125.216:8004/docs | **AI engine** — test failure analysis live |
| http://13.232.125.216:5000 | MLflow — model registry, training runs |
| http://13.232.125.216:3001 | Grafana — system monitoring |
| http://13.232.125.216:9090 | Prometheus — raw metrics |

### Test the AI right now

POST to `http://13.232.125.216:8004/api/v1/predict`:

```json
{
  "log_text": "ModuleNotFoundError: No module named 'requests'\nFAILED tests/test_api.py - AssertionError",
  "metadata": {"repo": "demo/project"}
}
```

Response:
```json
{
  "category": "dependency_error",
  "confidence": 0.70,
  "root_cause": "A required package could not be found or installed.",
  "suggestion": "Add requests to requirements.txt and run pip install.",
  "method": "rule_based"
}
```

---

## Pricing

| Plan | Price | Analyses/month | Repos |
|------|-------|---------------|-------|
| Free | $0 | 50 | 1 |
| Starter | $29/mo | 500 | 5 |
| Pro | $99/mo | Unlimited | Unlimited |

---

## Project Structure
## AI Pipeline — 3 Stages of Intelligence

| Stage | When | Method | Accuracy |
|-------|------|--------|----------|
| 1 — Rule-based | Day 0 | 20 regex patterns, 6 categories | ~68% |
| 2 — LLM | Week 2+ | AWS Bedrock structured prompt | ~88% |
| 3 — Fine-tuned | Month 2+ | DistilBERT trained on real data | ~93% |

The model **self-improves every Sunday** — engineer feedback becomes labeled training data, the model retrains on SageMaker, and only promotes to Production if F1 score improves by >2%.

---

## Failure Categories

CIPHER classifies pipeline failures into 6 categories:

| Category | Example |
|----------|---------|
| `test_failure` | `FAILED tests/test_auth.py - AssertionError` |
| `dependency_error` | `ModuleNotFoundError: No module named requests` |
| `build_error` | `SyntaxError: invalid syntax line 42` |
| `auth_failure` | `Permission denied: credentials invalid` |
| `infra_error` | `Connection refused: dial tcp :5432` |
| `timeout` | `Job exceeded maximum time limit` |

---

## Quick Start

```bash
git clone https://github.com/ansh9197/Cipher.git
cd Cipher
./scripts/start-all.sh
```

---

## Live Demo

| URL | What you see |
|-----|-------------|
| http://13.232.125.216:3000 | Product — register and explore dashboard |
| http://13.232.125.216:8001/docs | Auth API — interactive Swagger docs |
| http://13.232.125.216:8004/docs | **AI engine** — test failure analysis live |
| http://13.232.125.216:5000 | MLflow — model registry, training runs |
| http://13.232.125.216:3001 | Grafana — system monitoring |
| http://13.232.125.216:9090 | Prometheus — raw metrics |

### Test the AI right now

POST to `http://13.232.125.216:8004/api/v1/predict`:

```json
{
  "log_text": "ModuleNotFoundError: No module named 'requests'\nFAILED tests/test_api.py - AssertionError",
  "metadata": {"repo": "demo/project"}
}
```

Response:
```json
{
  "category": "dependency_error",
  "confidence": 0.70,
  "root_cause": "A required package could not be found or installed.",
  "suggestion": "Add requests to requirements.txt and run pip install.",
  "method": "rule_based"
}
```

---

## Pricing

| Plan | Price | Analyses/month | Repos |
|------|-------|---------------|-------|
| Free | $0 | 50 | 1 |
| Starter | $29/mo | 500 | 5 |
| Pro | $99/mo | Unlimited | Unlimited |

---

## Project Structure
cipher/
├── services/
│   ├── auth-service/           # JWT, Stripe, PostgreSQL
│   ├── webhook-service/        # GitHub webhook handler
│   ├── analysis-service/       # Log parser + Kafka
│   ├── inference-service/      # AI engine + MLflow
│   ├── notification-service/   # PR commenter + feedback
│   ├── retraining-job/         # Weekly ML retraining
│   └── mlflow-server/          # MLflow + psycopg2
├── frontend/                   # Next.js 14 SaaS dashboard
├── k8s/                        # Kubernetes manifests
├── terraform/production/       # AWS IaC (9 files)
├── monitoring/                 # Prometheus + Grafana
├── scripts/                    # start-all.sh, retrain.sh
└── docker-compose.yml          # Local development
---

## Built With

- **AWS** — EC2, S3, RDS, ElastiCache, ECR
- **Kubernetes** — k3s with HPA, CronJobs, ConfigMaps, Secrets
- **Terraform** — VPC, subnets, security groups, RDS, ElastiCache, S3, ECR
- **MLflow** — Experiment tracking + model registry + promotion gates
- **GitHub Actions** — Automated test + build + deploy on every push
- **Prometheus + Grafana** — Full observability stack

---

## What this project proves

This is not a tutorial project. It is a production SaaS with:

- **Multi-tenancy** — every user's data is isolated by tenant_id
- **Self-healing AI** — model improves automatically from feedback
- **Zero-downtime deploys** — Kubernetes rolling updates
- **Cost control** — plans enforce analysis limits via Redis rate limiting
- **Security** — HMAC webhook validation, JWT auth, bcrypt passwords
- **Observability** — every service scraped by Prometheus, dashboards in Grafana
