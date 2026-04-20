import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table('expenses')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    method = event['httpMethod']
    path = event['path']

    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    # POST /expenses - Add expense
    if method == 'POST' and path == '/expenses':
        body = json.loads(event['body'])
        expense = {
            'id': str(uuid.uuid4()),
            'date': body.get('date', str(datetime.now().date())),
            'amount': str(body['amount']),
            'category': body['category'],
            'description': body['description']
        }
        table.put_item(Item=expense)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Expense added', 'expense': expense})
        }

    # GET /expenses - View all expenses
    if method == 'GET' and path == '/expenses':
        result = table.scan()
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result['Items'])
        }

    # GET /expenses/summary - Summary by category
    if method == 'GET' and path == '/expenses/summary':
        result = table.scan()
        summary = {}
        for e in result['Items']:
            cat = e['category']
            amount = float(e['amount'])
            summary[cat] = summary.get(cat, 0) + amount
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(summary)
        }

    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({'message': 'Route not found'})
    }