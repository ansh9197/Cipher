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
<img width="957" height="763" alt="image" src="https://github.com/user-attachments/assets/1eb42a02-1428-4200-809a-60cf37f12336" />
---

## 🚀 CIPHER Tech Stack

| Category                     | Technologies Used |
|-----------------------------|-------------------|
| **Cloud Platform**          | AWS (EKS, EC2, SageMaker) |
| **Containerization**        | Docker |
| **Container Orchestration** | Kubernetes |
| **Infrastructure as Code**  | Terraform |
| **CI/CD Automation**        | Jenkins, GitHub Actions |
| **GitOps Deployment**       | Argo CD |
| **Programming Language**    | Python |
| **Machine Learning / AIOps**| AWS SageMaker, MLflow |
| **Monitoring & Observability** | Prometheus, Grafana |
| **Version Control**         | Git, GitHub |
| **Operating System**        | Linux (Ubuntu) |
| **Architecture Style**      | Cloud-Native Microservices |
| **Core Concepts**           | CI/CD, AIOps, Infrastructure Automation, Self-Healing Pipelines, MLOps |

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
## 📂 Project Structure

```bash
CIPHER/
│
├── .github/                          # GitHub Actions workflows
│   └── workflows/
│       ├── build-push.yml
│       └── deploy.yml
│
├── docs/                             # Documentation & architecture
│   ├── cipher-architecture.html
│   └── README.md
│
├── frontend/                         # Next.js frontend dashboard
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/
│   │   │   ├── login/
│   │   │   ├── pricing/
│   │   │   └── register/
│   │   │
│   │   └── lib/
│   │       ├── api.ts
│   │       └── auth.ts
│   │
│   ├── Dockerfile
│   ├── package.json
│   └── tailwind.config.js
│
├── k8s/                              # Kubernetes manifests
│   ├── configmaps/
│   ├── cronjobs/
│   ├── deployments/
│   ├── hpa/
│   ├── ingress/
│   ├── namespaces/
│   ├── secrets/
│   └── services/
│
├── monitoring/                       # Monitoring & observability stack
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── datasources/
│   │
│   ├── docker-compose.monitoring.yml
│   └── prometheus.yml
│
├── scripts/                          # Automation & utility scripts
│   ├── retrain.sh
│   ├── start-all.sh
│   └── status.sh
│
├── services/                         # Microservices architecture
│   ├── analysis-service/             # CI/CD log analysis service
│   ├── auth-service/                 # Authentication & user management
│   ├── inference-service/            # ML inference engine
│   ├── mlflow-server/                # MLflow tracking server
│   ├── notification-service/         # GitHub feedback & notifications
│   ├── retraining-job/               # Model retraining pipeline
│   └── webhook-service/              # GitHub webhook listener
│
├── terraform/                        # Infrastructure as Code
│   └── production/
│       ├── ec2.tf
│       ├── ecr.tf
│       ├── elasticache.tf
│       ├── rds.tf
│       ├── s3.tf
│       ├── security_groups.tf
│       ├── vpc.tf
│       └── main.tf
│
├── .env.example                      # Environment variables template
├── .gitignore
├── docker-compose.yml                # Multi-container local setup
├── Makefile                          # Automation commands
└── README.md
```




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
