import boto3
import json
 
dynamodb = boto3.client('dynamodb')
table_name = 'Inventory'
 
def lambda_handler(event, context):
    # Extract both keys from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters'] or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' in path parameters")
        }
 
    key = {
        'id': {'S': event['pathParameters']['id']},
        'location_id': {'N': event['pathParameters']['location_id']}
    }
 
    try:
        dynamodb.delete_item(TableName=table_name, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {event['pathParameters']['id']} deleted successfully.")
        }
 
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }