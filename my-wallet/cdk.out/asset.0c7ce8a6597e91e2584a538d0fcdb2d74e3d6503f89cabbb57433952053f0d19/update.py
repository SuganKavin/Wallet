import json
import logging
import os
import uuid
import boto3

from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])

    id  = event['pathParameters']['id']

    if not id:
        logging.error("Validation Failed. Missing id")
        raise Exception("Couldn't create the account.")

    if 'profileId' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the account.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    try:
        # update the account in the database
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            ExpressionAttributeValues={
                ':as': data['accountStatus'],
                ':ou': data['orgUnitId'],
                ':wt': data['workerType'],
                ':op': data['orgPersonId'],
                ':ae': data['accountEmail'],
                ':se': data['supervisorEmail'],
                ':or': data['orgPersonRole'],
                ':pl': data['personLocation'],
                ':wi': data['workIds'],
                ':ua': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            },
            UpdateExpression='SET accountStatus = :as, orgUnitId = :ou, workerType = :wt, orgPersonId = :op, accountEmail = :ae, '
                             'supervisorEmail = :se, orgPersonRole = :or, personLocation = :pl, workIds = list_append(workIds, :wi), updatedAt = :ua',
            ReturnValues='ALL_NEW',
        )
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'])
        }
    except ClientError as ex:
        response = {
            "statusCode": 400,
            "body": json.dumps(ex.response['Error']['Message'])
        }

    return response