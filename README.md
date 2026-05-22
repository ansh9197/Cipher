# CIPHER — CI/CD Intelligent Pipeline Health Engine with Autonomous Retraining
It is an AIOps-driven cloud-native platform designed to monitor CI/CD pipelines, detect failures, analyze root causes, and improve deployment reliability using monitoring and ML-based workflows. The platform was deployed on AWS EKS using Kubernetes and Docker containers, while Terraform handled infrastructure provisioning. Prometheus and Grafana were used for monitoring and visualization. MLflow and Sage Maker were integrated for model management and retraining workflows. The primary goal of the project was to reduce manual debugging efforts in CI/CD pipelines, improve deployment reliability, and create a scalable self-monitoring DevOps environment.
An AI-powered DevOps SaaS that automatically analyzes CI/CD pipeline failures and posts Plain-English root cause + fix suggestions as GitHub PR comments — within 30 seconds.

<img width="1314" height="585" alt="image" src="https://github.com/user-attachments/assets/6d6f2113-8b1d-4912-8d27-a7bfaed428d2" />

> An AI-powered DevOps SaaS that automatically analyzes CI/CD pipeline failures and posts plain-English root cause + fix suggestions as GitHub PR comments — within 30 seconds.
---


## ## 📊 CIPHER Dashboard Preview


<img width="860" height="482" alt="image" src="https://github.com/user-attachments/assets/93ca09b6-7259-4fd7-b97d-a690d340cde4" />




<img width="1333" height="605" alt="image" src="https://github.com/user-attachments/assets/fa9df260-3f49-4c5f-adc2-49e338e1bc5f" />

>Disclaimer: The dashboard preview shown above is for demonstration purposes only and represents CIPHER during its training and development phase. Certain predictions, pipeline analyses, logs, and AI-generated insights may not reflect fully optimized or production-accurate results. The displayed data is sample/test data intended to showcase the platform’s interface, architecture, and workflow capabilities.
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
## Security-Privacy
This ensures the platform monitors pipeline behavior without exposing proprietary source code or sensitive repository content.
The database architecture was also intentionally designed with minimal data retention principles. The users table stores only essential account information such as email address,  -hashed password, subscription plan, GitHub username, and monthly analysis count. Passwords are securely hashed using bcrypt and are irreversible.

<img width="665" height="612" alt="image" src="https://github.com/user-attachments/assets/a9623007-09d3-4ba4-921d-26aaa41e79b8" />





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


# ⚙️ Working of CIPHER

CIPHER works as an AI-powered DevOps intelligence platform that continuously monitors CI/CD pipelines, analyzes failures, and provides automated insights and remediation suggestions in real time.

---

## 🔄 Step-by-Step Working Flow

### 1️⃣ Developer Pushes Code
The workflow begins when a developer pushes code changes to a GitHub repository.

- GitHub triggers CI/CD pipeline events.
- Build, deployment, and workflow logs are generated automatically.

---

### 2️⃣ Webhook Captures Pipeline Events
The **Webhook Service** listens to GitHub webhook events.

It captures:
- repository activity
- workflow execution status
- deployment events
- build failures
- pull request activity

The captured data is then forwarded to Kafka for distributed event processing.

---

### 3️⃣ Kafka Streams Real-Time Events
Apache Kafka acts as the communication backbone between microservices.

Kafka distributes:
- CI/CD logs
- workflow metadata
- deployment events
- runtime information

to different internal services for parallel processing.

---

### 4️⃣ Analysis Service Processes Logs
The **Analysis Service** consumes pipeline logs from Kafka and performs:

- log parsing
- failure pattern detection
- error extraction
- anomaly identification
- deployment issue analysis

This service converts raw CI/CD logs into structured analytical data.

---

### 5️⃣ AI Inference Engine Predicts Failures
The processed data is sent to the **Inference Service**.

The ML inference engine:
- analyzes historical pipeline patterns
- detects recurring failures
- predicts root causes
- classifies failure severity
- generates intelligent remediation suggestions

This enables proactive DevOps troubleshooting instead of manual debugging.

---

### 6️⃣ Notification Service Generates Feedback
After analysis is completed:

The **Notification Service**:
- generates automated responses
- creates GitHub feedback comments
- sends failure summaries
- provides suggested fixes and debugging insights

This helps developers quickly identify and resolve deployment issues.

---

### 7️⃣ Dashboard Visualizes System Activity
The frontend dashboard displays:
- pipeline execution status
- detected failures
- AI-generated predictions
- deployment analytics
- monitoring metrics
- infrastructure health

This provides centralized visibility into the entire CI/CD ecosystem.

---

### 8️⃣ Monitoring & Observability
CIPHER continuously monitors infrastructure and services using:

- Prometheus
- Grafana
- Kubernetes monitoring

The monitoring stack tracks:
- container health
- API latency
- CPU & memory usage
- service uptime
- deployment performance

---

### 9️⃣ Model Retraining Pipeline
The **Retraining Job** periodically retrains ML models using newly collected CI/CD data.

This improves:
- prediction accuracy
- anomaly detection
- recommendation quality
- failure classification performance

MLflow is used for:
- model tracking
- experiment management
- model versioning

---

## ☁️ Infrastructure Workflow

CIPHER is fully cloud-native and deployed using:

- Docker containers
- Kubernetes orchestration
- Terraform infrastructure provisioning
- AWS cloud services

The infrastructure includes:
- EC2
- ECR
- RDS
- ElastiCache
- VPC networking
- Kubernetes workloads

---

## 🔁 Complete Execution Flow

```text
Developer Push
      ↓
GitHub Webhook Trigger
      ↓
Webhook Service
      ↓
Kafka Event Streaming
      ↓
Analysis Service
      ↓
AI Inference Engine
      ↓
Failure Prediction & Insights
      ↓
Notification Service
      ↓
GitHub Feedback + Dashboard Visualization
      ↓
Monitoring & Observability
```

---

## 🎯 End Result

CIPHER automates the process of:
- monitoring CI/CD pipelines
- detecting deployment failures
- analyzing logs intelligently
- predicting root causes
- generating remediation suggestions
- visualizing infrastructure and deployment health

This reduces manual debugging effort and improves deployment reliability in modern DevOps environments.
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
## 💳 CIPHER Pricing Plans

CIPHER provides flexible subscription plans designed for individual developers, growing teams, and enterprise-scale DevOps environments. The platform offers AI-powered CI/CD failure analysis, intelligent debugging insights, automated GitHub feedback, and scalable infrastructure monitoring.

<img width="1163" height="592" alt="image" src="https://github.com/user-attachments/assets/c7767bce-b2be-4d9b-b98e-f0a3f27f497a" />

### 🔹 Available Plans
| Plan | Features |
|---|---|
| **Free** | 50 analyses/month, 1 repository, GitHub PR comments |
| **Starter** | 500 analyses/month, 5 repositories, Slack integration, Email alerts |
| **Pro** | Unlimited analyses, unlimited repositories, custom AI models, API access |

>**Disclaimer:** The pricing plans, features, and subscription values displayed above are part of a demonstration prototype created for showcasing the platform architecture and product vision of CIPHER. These prices and offerings are illustrative and may not represent final production or commercial pricing.
---


---
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
