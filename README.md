# CIPHER — CI/CD Intelligent Pipeline Health Engine with Autonomous Retraining

> An AI-powered DevOps SaaS that automatically analyzes CI/CD pipeline failures and posts plain-English root cause + fix suggestions as GitHub PR comments — within 30 seconds, before the developer even opens their laptop.

![Architecture](https://img.shields.io/badge/Architecture-Microservices-6366f1)
![AI](https://img.shields.io/badge/AI-Self--Improving-10b981)
![K8s](https://img.shields.io/badge/Kubernetes-k3s-326ce5)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)

## What CIPHER Does

1. **Detects** — GitHub Actions webhook fires when a pipeline fails
2. **Analyzes** — Downloads logs, cleans noise, extracts error signals
3. **Classifies** — AI engine categorizes the failure (test/dependency/build/auth/infra/timeout)
4. **Explains** — Posts root cause + fix suggestion as a PR comment
5. **Learns** — Engineer feedback (👍/👎) trains the model weekly via MLflow

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI (5 microservices) |
| Frontend | Next.js 14, React, Tailwind CSS |
| AI/ML | TF-IDF + LogReg → DistilBERT fine-tuning, MLflow |
| Messaging | Apache Kafka |
| Database | PostgreSQL (SQLAlchemy async) |
| Cache | Redis |
| Container | Docker, Docker Compose |
| Orchestration | Kubernetes (k3s) with HPA |
| IaC | Terraform (VPC, RDS, ElastiCache, S3, ECR) |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Billing | Stripe |

## Architecture


cat > ~/cipher/README.md << 'EOF'
# CIPHER — CI/CD Intelligent Pipeline Health Engine with Autonomous Retraining

> An AI-powered DevOps SaaS that automatically analyzes CI/CD pipeline failures and posts plain-English root cause + fix suggestions as GitHub PR comments — within 30 seconds, before the developer even opens their laptop.

![Architecture](https://img.shields.io/badge/Architecture-Microservices-6366f1)
![AI](https://img.shields.io/badge/AI-Self--Improving-10b981)
![K8s](https://img.shields.io/badge/Kubernetes-k3s-326ce5)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)

## What CIPHER Does

1. **Detects** — GitHub Actions webhook fires when a pipeline fails
2. **Analyzes** — Downloads logs, cleans noise, extracts error signals
3. **Classifies** — AI engine categorizes the failure (test/dependency/build/auth/infra/timeout)
4. **Explains** — Posts root cause + fix suggestion as a PR comment
5. **Learns** — Engineer feedback (👍/👎) trains the model weekly via MLflow

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI (5 microservices) |
| Frontend | Next.js 14, React, Tailwind CSS |
| AI/ML | TF-IDF + LogReg → DistilBERT fine-tuning, MLflow |
| Messaging | Apache Kafka |
| Database | PostgreSQL (SQLAlchemy async) |
| Cache | Redis |
| Container | Docker, Docker Compose |
| Orchestration | Kubernetes (k3s) with HPA |
| IaC | Terraform (VPC, RDS, ElastiCache, S3, ECR) |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Billing | Stripe |

## Architecture
## Microservices

| Service | Port | Responsibility |
|---------|------|---------------|
| auth-service | 8001 | JWT auth, user management, Stripe billing |
| webhook-service | 8002 | GitHub webhook receiver, HMAC validation |
| analysis-service | 8003 | Log parser, GitHub API client, Kafka consumer |
| inference-service | 8004 | AI classification engine, MLflow model loading |
| notification-service | 8005 | PR comment poster, feedback collection |
| frontend | 3000 | Next.js dashboard, landing page, pricing |
| mlflow | 5000 | Model registry, experiment tracking |

## AI Pipeline — 3 Stages

| Stage | When | Method | Accuracy |
|-------|------|--------|----------|
| 1 — Rule-based | Day 0 | Regex patterns | ~68% |
| 2 — LLM | Week 2+ | AWS Bedrock / OpenAI | ~88% |
| 3 — Fine-tuned | Month 2+ | DistilBERT on real data | ~93% |

## Quick Start

```bash
# Clone
git clone https://github.com/ansh9197/Cipher.git
cd Cipher

# Start everything
./scripts/start-all.sh
```

## Live Demo

| URL | Description |
|-----|-------------|
| http://13.232.125.216:3000 | Product landing page |
| http://13.232.125.216:8001/docs | Auth API (Swagger) |
| http://13.232.125.216:8004/docs | AI inference API |
| http://13.232.125.216:5000 | MLflow model registry |
| http://13.232.125.216:3001 | Grafana monitoring |

## Pricing

| Plan | Price | Analyses/month |
|------|-------|---------------|
| Free | $0 | 50 |
| Starter | $29/mo | 500 |
| Pro | $99/mo | Unlimited |

## Project Structure
| URL | Description |
|-----|-------------|
| http://13.232.125.216:3000 | Product landing page |
| http://13.232.125.216:8001/docs | Auth API (Swagger) |
| http://13.232.125.216:8004/docs | AI inference API |
| http://13.232.125.216:5000 | MLflow model registry |
| http://13.232.125.216:3001 | Grafana monitoring |

## Pricing

| Plan | Price | Analyses/month |
|------|-------|---------------|
| Free | $0 | 50 |
| Starter | $29/mo | 500 |
| Pro | $99/mo | Unlimited |

## Project Structure
cipher/
├── services/
│   ├── auth-service/          # JWT, Stripe, PostgreSQL
│   ├── webhook-service/       # GitHub webhook handler
│   ├── analysis-service/      # Log parser + Kafka consumer
│   ├── inference-service/     # AI engine + MLflow
│   ├── notification-service/  # PR commenter + feedback
│   ├── retraining-job/        # Weekly ML retraining
│   └── mlflow-server/         # MLflow with psycopg2
├── frontend/                  # Next.js 14 SaaS dashboard
├── k8s/                       # Kubernetes manifests
├── terraform/production/      # AWS infrastructure as code
├── monitoring/                # Prometheus + Grafana
├── scripts/                   # Startup + utility scripts
└── docker-compose.yml         # Local development
## Built With

- **AWS** — EC2, S3, RDS, ElastiCache, ECR, SageMaker
- **Kubernetes** — k3s with HPA, CronJobs, ConfigMaps
- **Terraform** — Complete IaC for production AWS
- **MLflow** — Model registry with automated promotion gates
- **GitHub Actions** — CI/CD build + deploy pipeline
