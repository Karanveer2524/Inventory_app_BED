import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def lambda_handler(event, context):
    if 'pathParameters' not in event or 'id' not in event['pathParameters'] or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' in path parameters")
        }

    id_value = event['pathParameters']['id']
    location_value = int(event['pathParameters']['location_id'])

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(id_value) & Key('location_id').eq(location_value)
        )
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        return {
            'statusCode': 200,
            'body': json.dumps(convert_decimals(items[0]))
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
