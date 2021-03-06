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

    trxTable = dynamodb.Table(os.environ['TRANSACTION_TABLE'])
    trxId = str(uuid.uuid1())
    item = {
        'id': trxId,
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
    trxTable.put_item(Item=item)


    walletTable = dynamodb.Table(os.environ['WALLET_TABLE'])

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
        "Balance": 0,
        "TrxDate":timestamp

    }

    #input ='#CurrentBalance'

    result = walletTable.update_item(
        Key={
            'id': data['SenderWalletId']
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

    result = walletTable.update_item(
        Key={
            'id': data['ReceiverWalletId']
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

'''
Needs to add
1. Transaction rollback needs be handle , since wallet update depends on the transaction creation
2. dynamic update into TrxHistory-Balance value with CurrentBalance
3. BWAL-trxAmt condition check handled by UI/service. [Condition BWAL >= trxAMT]
4. Trx date is stored as decimal. Needs to be fixed
'''