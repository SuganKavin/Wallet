import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    if 'Item' in result:
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'])
        }
    else:
        response = {
            "statusCode": 400,
            "body": json.dumps("account not available")
        }
    return response