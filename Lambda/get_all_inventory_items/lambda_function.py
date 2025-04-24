import boto3
import json

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Set your table name
    table_name = 'Inventory'

    try:
        # Scan the table
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        # Return result
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
