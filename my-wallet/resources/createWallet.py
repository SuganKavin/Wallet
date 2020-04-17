import json
import logging
import os
import time
import uuid
import logging
import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['WALLET_TABLE'])

    wallet_bwal ={
        'WalletCurrency': data['WalletCurrency'],
        'AccountId': data['AccountId'],
        'CurrentReservedBalance': 0,
        'WalletType': 'BWAL',
        'CurrentBalance': 0,
        'WalletId': str(uuid.uuid1())
    }
    wallet_pwal ={
        'WalletCurrency': data['WalletCurrency'],
        'AccountId': data['AccountId'],
        'CurrentReservedBalance': 0,
        'WalletType': 'PWAL',
        'CurrentBalance': 0,
        'WalletId': str(uuid.uuid1())
    }

    logging.info(wallet_bwal)
    logging.info(wallet_pwal)
    with table.batch_writer() as batch:
        batch.put_item(
            Item= wallet_bwal)
        batch.put_item(
            Item= wallet_pwal)



    # create a response
    response = {
        "statusCode": 200
    }

    return response
