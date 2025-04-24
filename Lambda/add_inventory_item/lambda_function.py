import json
import boto3
import uuid
from decimal import Decimal
 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')
 
def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }
 
    # Generate a unique ID for the item
    unique_id = str(uuid.uuid4())
 
    # Required fields check
    required_fields = ['name', 'description', 'price', 'quantity', 'location_id']
    if not all(field in data for field in required_fields):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing one or more required fields: " + ", ".join(required_fields))
        }
 
    try:
        # Insert data into DynamoDB
        table.put_item(
            Item={
                'id': unique_id,
                'location_id': int(data['location_id']),
                'name': data['name'],
                'description': data['description'],
                'price': Decimal(str(data['price'])),  # handle float-to-Decimal conversion
                'quantity': int(data['quantity'])
            }
        )
        return {
            'statusCode': 201,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
 
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
 
 