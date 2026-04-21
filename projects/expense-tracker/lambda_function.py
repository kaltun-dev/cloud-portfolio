import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table('expenses')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }

    method = event.get('httpMethod', '')
    path = event.get('path', '')

    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    try:
        if method == 'POST' and 'expenses' in path:
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

        if method == 'GET' and 'summary' in path:
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

        if method == 'GET' and 'expenses' in path:
            result = table.scan()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result['Items'])
            }

        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'message': f'Route not found: {method} {path}'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }