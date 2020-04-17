import json
import logging
import os
import time
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])
    '''if 'profileId' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the account.")'''

    timestamp = str(time.time())

    trx_table = dynamodb.Table(os.environ['TRANSACTION_TABLE'])
    trxId = str(uuid.uuid1())
    item = {
        'TrxId': trxId,
        'OrgId': data['OrgId'],
        'SenderWalletId': data['SenderWalletId'],
        'ReceiverWalletId': data['ReceiverWalletId'],
        'TrxDate': timestamp,
        'TrxType': data['TrxType'],
        'Reason': data['Reason'],
        'TrxAmount': data['TrxAmount'],
        'TrxCurrency': data['TrxCurrency'],
        'TrxComments': data['TrxComments'],
    }

    # write the account to the database
    trx_table.put_item(Item=item)


    wallet_table = dynamodb.Table(os.environ['WALLET_TABLE'])

    senderTrxHistory ={

        "TrxId": trxId,
        "TrxType": data['TrxType'],
        "TrxAmount": data['TrxAmount'],
        "Balance": 40,
        "TrxDate":timestamp

    }

    receiverTrxHistory ={

        "TrxId": trxId,
        "TrxType": data['TrxType'],
        "TrxAmount": data['TrxAmount'],
        "Balance": 40,
        "TrxDate":timestamp

    }

    #nput ='#CurrentBalance'

    result = wallet_table.update_item(
        Key={
            'WalletId': data['SenderWalletId']
        },
        UpdateExpression= "SET CurrentBalance = CurrentBalance - :TrxAmount,TrxHistory = list_append(if_not_exists(TrxHistory, :empty_list), :TrxHistory)",
        ExpressionAttributeValues={
            ':TrxHistory': [{

                "TrxId": trxId,
                "TrxType": data['TrxType'],
                "TrxAmount": data['TrxAmount'],
                "Balance": 0,
                "TrxDate":timestamp

            }],
            ':empty_list':[],
            ':TrxAmount':data['TrxAmount']
        },
        ReturnValues="UPDATED_NEW"
    )

    result = wallet_table.update_item(
        Key={
            'WalletId': data['ReceiverWalletId']
        },
        UpdateExpression= "SET CurrentBalance = CurrentBalance + :TrxAmount, TrxHistory = list_append(if_not_exists(TrxHistory, :empty_list), :TrxHistory)",
        ExpressionAttributeValues={
            ':TrxHistory': [receiverTrxHistory],
            ':empty_list':[],
            ':TrxAmount':data['TrxAmount']
        },
        ReturnValues="UPDATED_NEW"
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
