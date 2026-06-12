# Cloud Portfolio

A live cloud engineering portfolio built and deployed entirely on AWS, managed with Terraform, and updated automatically through a CI/CD pipeline.

**Live site:** https://kaltun.co.uk

## About

This portfolio was built to demonstrate practical, hands-on AWS skills including cloud support, troubleshooting, infrastructure setup, and basic automation. Every project here is live on AWS, not a local demo, and the infrastructure that hosts the site itself is part of the portfolio, showing real experience with deploying, configuring, and fixing cloud resources.

## Live Architecture

```
                         ┌─────────────────────┐
                         │   Route 53           │
                         │   kaltun.co.uk        │
                         └──────────┬───────────┘
                                     │
                         ┌──────────▼───────────┐
                         │   ACM Certificate     │
                         │   (us-east-1)         │
                         └──────────┬───────────┘
                                     │
                         ┌──────────▼───────────┐
                         │   CloudFront          │
                         │   EJNQOYSHP4HLB       │
                         └──────────┬───────────┘
                                     │
                         ┌──────────▼───────────┐
                         │   S3 Static Hosting   │
                         │   cloud-portfolio-    │
                         │   frontend            │
                         └───────────────────────┘

  Expense Tracker:   API Gateway → Lambda → DynamoDB
  Weather Dashboard: API Gateway V2 → Lambda → SSM Parameter Store → OpenWeatherMap
```

## Projects

| Project | Description | Tech |
|---|---|---|
| [Expense Tracker](projects/expense-tracker) | Serverless app to log and summarise expenses | Lambda, API Gateway, DynamoDB, Python |
| [Weather Dashboard](projects/weather-dashboard) | Live weather lookup by city | Lambda, API Gateway V2, SSM Parameter Store |
| [Linux Quiz App](projects/Ci-Quiz-App) | Interactive Linux command line quiz | HTML, CSS, JavaScript |
| Cloud Infrastructure | The infrastructure behind this entire portfolio | Terraform, S3, CloudFront, Route 53, IAM |

## Infrastructure Currently in Use

- **Amazon S3** — static website hosting for the frontend and all project files
- **Amazon CloudFront** — global content delivery network with HTTPS
- **Route 53** — custom domain (`kaltun.co.uk` and `www.kaltun.co.uk`) with DNS management
- **AWS Certificate Manager** — free SSL/TLS certificate for HTTPS, requested in us-east-1 for CloudFront compatibility
- **AWS Lambda** — serverless compute for the Expense Tracker and Weather Dashboard
- **Amazon API Gateway** (REST and HTTP APIs) — request routing to Lambda
- **Amazon DynamoDB** — NoSQL database for the Expense Tracker
- **AWS Systems Manager Parameter Store** — secure storage for the OpenWeatherMap API key
- **AWS IAM** — least-privilege roles and policies for each Lambda function
- **Amazon CloudWatch** — billing alarm that emails an alert if AWS charges exceed a set threshold, using an SNS topic (`billing-alarm`) in us-east-1
- **Terraform** — infrastructure as code, with remote state stored and versioned in an S3 bucket (`kaltun-terraform-state`)
- **GitHub Actions** — CI/CD pipeline that syncs the frontend and all project directories to S3 and invalidates the CloudFront cache on every push to `main`

## Infrastructure Planned / In Progress

- **AWS WAF** — a web application firewall attached to CloudFront for an extra layer of security, especially relevant for security-focused roles
- **Session-based data isolation** — separating expense data per visitor so the Expense Tracker is not shared globally
- **Next project: containerised redeployment** — redeploying this same portfolio using a VPC with public and private subnets, EC2 instances, an Application Load Balancer, an Auto Scaling Group, RDS for the database layer, and Docker images stored in ECR, all provisioned with Terraform modules

## CI/CD Pipeline

Every push to the `main` branch triggers a GitHub Actions workflow that:

1. Syncs the `frontend/` directory and every project under `projects/` to the S3 bucket `cloud-portfolio-frontend`
2. Invalidates the CloudFront cache so changes appear immediately rather than waiting for the cache to expire

## Infrastructure as Code

Core infrastructure is managed with Terraform, with state stored remotely in S3 with versioning enabled so changes can be tracked and rolled back if needed. Resources that were originally created manually, such as the Expense Tracker's Lambda function, API Gateway, DynamoDB table, and IAM role, have since been imported into Terraform state so they are fully managed going forward.

## Troubleshooting Log

A full log of real issues encountered and fixed throughout this project, including WSL networking problems on ARM64, Terraform import edge cases, IAM role path mismatches, Lambda proxy integration errors, and Git history rewrites, is documented on the live site under the Troubleshooting section.

## Tech Stack

AWS (S3, CloudFront, Lambda, API Gateway, DynamoDB, Route 53, ACM, CloudWatch, SNS, SSM Parameter Store, IAM), Terraform, Python, JavaScript, HTML, CSS, GitHub Actions, Git, Linux, AWS CLI

## Certifications

- AWS re/Start — Graduated May 2026
- AWS Certified Cloud Practitioner — In Progress
- AWS Certified Solutions Architect Associate — In Progress

## Contact

- GitHub: [kaltun-dev](https://github.com/kaltun-dev)
- LinkedIn: [Kaltun Osman](https://www.linkedin.com/in/kaltun-osman)

---

Built with AWS and Terraform · eu-west-2 · London