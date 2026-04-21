# cloud-portfolio
# ☁️ Cloud Portfolio — Kaltun

A full-stack cloud portfolio built and deployed entirely on AWS, showcasing serverless architecture, infrastructure as code, and frontend development skills.

🌐 **Live:** [cloud-portfolio-frontend.s3-website.eu-west-2.amazonaws.com](http://cloud-portfolio-frontend.s3-website.eu-west-2.amazonaws.com)

---

## 🏗️ Architecture

```
                    ┌─────────────┐
                    │  CloudFront │  (CDN + HTTPS)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │     S3      │  (Static hosting)
                    └─────────────┘
                    
┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser    │───▶│ API Gateway │───▶│   Lambda    │
└──────────────┘    └─────────────┘    └──────┬──────┘
                                              │
                                       ┌──────▼──────┐
                                       │   DynamoDB  │
                                       └─────────────┘
```

**AWS Services Used:**
- **S3** — Static website hosting for portfolio and project frontends
- **CloudFront** — CDN with HTTPS in front of S3
- **Lambda** — Serverless Python functions for backend logic
- **API Gateway** — REST API endpoints for Lambda functions
- **DynamoDB** — NoSQL database for expense tracker data
- **IAM** — Roles and policies for least-privilege access
- **Terraform** — All infrastructure provisioned as code with remote S3 backend

---

## 📁 Projects

### 1. 💰 Expense Tracker
A serverless expense tracking application built with Python and AWS.

**Features:**
- Add expenses with date, amount, category and description
- View all expenses in a table
- Delete individual expenses
- Clear all expenses
- Summary by category

**Stack:** Python · Lambda · API Gateway · DynamoDB · S3

**Live:** [View Project](http://cloud-portfolio-frontend.s3-website.eu-west-2.amazonaws.com/projects/expense-tracker/index.html)

---

### 2. 🐧 Linux Quiz App
An interactive quiz testing Linux command line knowledge with 50 questions.

**Features:**
- Choose between 5, 10, 20 or 50 questions
- Randomised question order every game
- Instant correct/wrong feedback
- Score tracking
- Play again functionality

**Stack:** JavaScript · CSS · HTML · S3 · CloudFront

**Live:** [View Project](http://cloud-portfolio-frontend.s3-website.eu-west-2.amazonaws.com/projects/linux-quiz/index.html)

---

### 3. 🌤️ Weather Dashboard
*(Coming Soon)*

Real-time weather data app powered by AWS Lambda and OpenWeatherMap API.

**Stack:** Python · Lambda · API Gateway · SSM Parameter Store

---

### 4. 🏗️ Cloud Infrastructure (Terraform)
The entire AWS infrastructure for this portfolio provisioned with Terraform.

**Features:**
- S3 buckets for static hosting
- CloudFront distribution
- Lambda functions
- API Gateway REST APIs
- DynamoDB tables
- IAM roles and policies
- Remote state stored in S3

**Stack:** Terraform · AWS · S3 Backend · GitHub

**Repo:** [View on GitHub](https://github.com/kaltun-dev/cloud-portfolio)

---

### 5. 🤖 CarbLens — AI Carb Analyzer
*(In Development)*

An AI-powered meal image scanner that analyses photos of food and returns structured carbohydrate estimates with confidence indicators.

**Stack:** Python · React · Anthropic API · Claude AI

---

## 🚀 Getting Started

### Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Python 3.12

### Deploy Infrastructure
```bash
# Clone the repo
git clone https://github.com/kaltun-dev/cloud-portfolio.git
cd cloud-portfolio/terraform

# Initialise Terraform
terraform init

# Preview changes
terraform plan

# Deploy
terraform apply
```

### Deploy Frontend
```bash
# Upload portfolio
aws s3 cp frontend/index.html s3://cloud-portfolio-frontend/index.html

# Upload expense tracker
aws s3 cp projects/expense-tracker/index.html \
  s3://cloud-portfolio-frontend/projects/expense-tracker/index.html

# Upload Linux quiz
aws s3 sync projects/Ci-Quiz-App/CI-Quiz-App/ \
  s3://cloud-portfolio-frontend/projects/linux-quiz/ --delete
```

### Deploy Lambda Functions
```bash
# Expense tracker
cd projects/expense-tracker
zip function.zip lambda_function.py
aws lambda update-function-code \
  --function-name expense-tracker \
  --zip-file fileb://function.zip \
  --region eu-west-2
```

---

## 📂 Project Structure

```
cloud-portfolio/
├── terraform/              # Infrastructure as Code
│   ├── main.tf             # S3 + CloudFront resources
│   ├── providers.tf        # AWS provider config
│   ├── backend.tf          # Remote S3 state backend
│   ├── variables.tf        # Input variables
│   └── outputs.tf          # Output values
├── frontend/
│   └── index.html          # Portfolio landing page
└── projects/
    ├── expense-tracker/
    │   ├── index.html      # Frontend UI
    │   └── lambda_function.py  # Backend logic
    ├── Ci-Quiz-App/        # Linux quiz app
    └── weather-dashboard/  # Coming soon
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Cloud | AWS (Lambda, S3, CloudFront, API Gateway, DynamoDB, IAM) |
| IaC | Terraform |
| Backend | Python 3.12 |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git, GitHub |
| OS | Linux (Ubuntu WSL) |

---

## 👩‍💻 About

**Kaltun** — AWS re/Start Graduate based in London.

- 🐙 GitHub: [kaltun-dev](https://github.com/kaltun-dev)
- 💼 LinkedIn: [linkedin.com/in/kaltun](https://linkedin.com/in/kaltun)

---

## 📋 Certifications (In Progress)

- 🎓 AWS re/Start
- ☁️ AWS Cloud Practitioner
- 🔐 CompTIA Security+

---

*Built with AWS + Terraform · eu-west-2 · London*