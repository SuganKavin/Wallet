import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')


def handler(event, context):

    table = dynamodb.Table(os.environ['WALLET_TABLE'])
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    '''result = table.query(
        KeyConditionExpression= Key('WalletId').eq("10001")
    )'''

    class DecimalEncoder(json.JSONEncoder):
        def default(self, result):
            if isinstance(result, Decimal):
                return float(result)
            return json.JSONEncoder.default(self, result)


    json.dumps(result, cls=DecimalEncoder)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response