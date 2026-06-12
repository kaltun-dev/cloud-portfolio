# Expense Tracker

A serverless expense tracking application built on AWS. Users can add expenses, view all transactions, get a spending summary by category, and clear all data. The entire backend runs without any servers, using Lambda, API Gateway, and DynamoDB.

**Live demo:** https://kaltun.co.uk/projects/expense-tracker/index.html

## Architecture

The frontend is a static HTML, CSS, and JavaScript page hosted on S3 and served through CloudFront. When a user adds, views, or deletes an expense, the page sends a request to API Gateway, which triggers a Lambda function. The Lambda function reads from and writes to a DynamoDB table.

```
Browser → CloudFront → S3 (frontend)
Browser → API Gateway → Lambda → DynamoDB
```

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** AWS Lambda (Python 3.12)
- **API:** Amazon API Gateway (REST API)
- **Database:** Amazon DynamoDB
- **Infrastructure as Code:** Terraform
- **Hosting:** Amazon S3 + CloudFront

## How It Works

The DynamoDB table `expenses` stores each expense as an item with a unique `id`, an amount, a category, and a date. The Lambda function `expense-tracker` handles four operations through the API:

- `GET /expenses` — returns all expenses
- `POST /expenses` — adds a new expense
- `DELETE /expenses/{id}` — deletes a single expense
- `DELETE /expenses/clear` — clears all expenses
- `GET /expenses/summary` — returns total spending grouped by category

## Infrastructure as Code

All resources for this project (DynamoDB table, IAM role, Lambda function, and API Gateway resources, methods, and integration) are managed with Terraform and imported into a remote state file stored in S3. The IAM role uses the `/service-role/` path to match how Lambda originally created it.

## Known Limitations

Currently all users share the same DynamoDB table, so expense data is not isolated per visitor. Session-based data isolation is a planned future improvement.

## Troubleshooting Highlights

A full troubleshooting log for this project, including issues like Lambda proxy integration misconfiguration and incorrect API paths, is documented on the main portfolio site under the Troubleshooting section.