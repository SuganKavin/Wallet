import json
import logging
import os
import time
import uuid
import boto3

from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])
    if 'profileId' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the account.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'profileId': data['profileId'],
        'orgId': data['orgId'],
        'accountStatus': data['accountStatus'],
        'orgUnitId': data['orgUnitId'],
        'workerType': data['workerType'],
        'orgPersonId': data['orgPersonId'],
        'accountEmail': data['accountEmail'],
        'supervisorEmail': data['supervisorEmail'],
        'orgPersonRole': data['orgPersonRole'],
        'personLocation': data['personLocation'],
        'workIds': data['workIds'],
        'createdAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'updatedAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }

    # write the account to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response