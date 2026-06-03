# Portfolio Frontend S3 Bucket
resource "aws_s3_bucket" "portfolio" {
  bucket = "${var.project_name}-frontend"

  tags = {
    Name        = "${var.project_name}-frontend"
    Environment = "production"
  }
}

resource "aws_s3_bucket_website_configuration" "portfolio" {
  bucket = aws_s3_bucket.portfolio.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "portfolio" {
  bucket = aws_s3_bucket.portfolio.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "portfolio" {
  bucket = aws_s3_bucket.portfolio.id
  depends_on = [aws_s3_bucket_public_access_block.portfolio]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.portfolio.arn}/*"
      }
    ]
  })
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "portfolio" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.portfolio.website_endpoint
    origin_id   = "S3-portfolio"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-portfolio"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name        = "${var.project_name}-cloudfront"
    Environment = "production"
  }
}

# DynamoDB Table - Expense Tracker
resource "aws_dynamodb_table" "expenses" {
  name         = "expenses"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "expenses"
    Environment = "production"
  }
}

# IAM Role - Expense Tracker Lambda
resource "aws_iam_role" "expense_tracker" {
  name = "expense-tracker-role-irnuy7qr"
  path = "/service-role/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "expense_tracker_dynamo" {
  role       = aws_iam_role.expense_tracker.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "expense_tracker_logs" {
  role       = aws_iam_role.expense_tracker.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function - Expense Tracker
resource "aws_lambda_function" "expense_tracker" {
  function_name = "expense-tracker"
  role          = aws_iam_role.expense_tracker.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  s3_bucket     = "kaltun-terraform-state"
  s3_key        = "lambda/expense-tracker.zip"

  tags = {
    Name        = "expense-tracker"
    Environment = "production"
  }
}

# API Gateway - Expense Tracker
resource "aws_api_gateway_rest_api" "expense_tracker" {
  name = "expense-tracker-api"
}

resource "aws_api_gateway_resource" "expenses" {
  rest_api_id = aws_api_gateway_rest_api.expense_tracker.id
  parent_id   = aws_api_gateway_rest_api.expense_tracker.root_resource_id
  path_part   = "expenses"
}

resource "aws_api_gateway_method" "expenses_get" {
  rest_api_id   = aws_api_gateway_rest_api.expense_tracker.id
  resource_id   = aws_api_gateway_resource.expenses.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "expenses_post" {
  rest_api_id   = aws_api_gateway_rest_api.expense_tracker.id
  resource_id   = aws_api_gateway_resource.expenses.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "expenses_delete" {
  rest_api_id   = aws_api_gateway_rest_api.expense_tracker.id
  resource_id   = aws_api_gateway_resource.expenses.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "expenses_options" {
  rest_api_id   = aws_api_gateway_rest_api.expense_tracker.id
  resource_id   = aws_api_gateway_resource.expenses.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "expenses_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.expense_tracker.id
  resource_id             = aws_api_gateway_resource.expenses.id
  http_method             = "POST"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.expense_tracker.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.expense_tracker.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.expense_tracker.execution_arn}/*/*"
}