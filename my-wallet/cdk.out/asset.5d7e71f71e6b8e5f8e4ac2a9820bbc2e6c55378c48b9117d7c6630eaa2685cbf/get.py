import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')


def handler(event, context):

    table = dynamodb.Table(os.environ['WALLET_TABLE'])
    result = table.get_item(
        Key={
            'WalletId': event['pathParameters']['id']
        }
    )
    '''result = table.query(
        KeyConditionExpression= Key('WalletId').eq("10001")
    )'''
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response