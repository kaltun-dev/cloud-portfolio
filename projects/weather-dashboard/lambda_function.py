import json
import urllib.request
import boto3

def lambda_handler(event, context):
    try:
        ssm = boto3.client('ssm', region_name='eu-west-2')
        parameter = ssm.get_parameter(
            Name='/weather-dashboard/openweathermap-api-key',
            WithDecryption=True
        )
        api_key = parameter['Parameter']['Value']

        body = json.loads(event.get('body', '{}'))
        city = body.get('city', 'London')

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=24"
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        forecasts = []
        seen_dates = []
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in seen_dates:
                seen_dates.append(date)
                forecasts.append({
                    'date': date,
                    'temp': round(item['main']['temp']),
                    'feels_like': round(item['main']['feels_like']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            if len(forecasts) == 3:
                break

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': forecasts
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }