# Weather Dashboard

A serverless weather lookup application. Users enter the name of any city and get the current temperature, humidity, and a short forecast, pulled live from the OpenWeatherMap API.

**Live demo:** https://kaltun.co.uk/projects/weather-dashboard/index.html

## Architecture

The frontend is a static HTML, CSS, and JavaScript page hosted on S3 and served through CloudFront. When a user searches for a city, the page calls API Gateway (HTTP API), which triggers a Lambda function. The Lambda function reads the OpenWeatherMap API key from SSM Parameter Store, calls the OpenWeatherMap API, and returns the weather data to the browser.

```
Browser → CloudFront → S3 (frontend)
Browser → API Gateway (HTTP API) → Lambda → SSM Parameter Store
                                          → OpenWeatherMap API
```

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** AWS Lambda (Python)
- **API:** Amazon API Gateway V2 (HTTP API)
- **Secrets management:** AWS Systems Manager Parameter Store
- **External API:** OpenWeatherMap
- **Hosting:** Amazon S3 + CloudFront

## How It Works

The Lambda function `weather-dashboard` is triggered through the `weather-dashboard-api` HTTP API. On each request, it retrieves the OpenWeatherMap API key securely from SSM Parameter Store rather than hardcoding it in the source code. This keeps the API key out of the codebase and out of version control. The function then queries OpenWeatherMap for the requested city and returns the temperature, humidity, and forecast as JSON to the frontend.

## Security Note

Storing the API key in SSM Parameter Store means the key is never committed to GitHub and can be rotated without changing any code. The Lambda execution role `weather-dashboard-role` is granted permission to read this specific parameter only.

## Planned Improvements

Docker and ECR integration for this project was considered but deferred in favour of keeping the deployment simple and low-cost. This may be revisited as part of a future containerised redeployment of the portfolio.