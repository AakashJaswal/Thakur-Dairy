import botocore.exceptions
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key
from common import render_response, user_table, table_name
import json

deserialize = TypeDeserializer().deserialize
event = {'Records': [{'eventID': '97e6a8c7bbf160902f1b8154483dbef0', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'us-east-1', 'dynamodb': {'ApproximateCreationDateTime': 1623004949.0, 'Keys': {'cache': {'S': 'account'}, 'PhoneNo': {'S': '123'}}, 'NewImage': {'cache': {'S': 'account'}, 'Address': {'S': 'Delhi'}, 'PhoneNo': {'S': '123'}, 'FirstName': {'S': 'sagar'}, 'Landmark': {'S': 'Near KV'}, 'LastName': {'S': 'jaswal'}, 'PlusCode': {'S': 'xyz'}}, 'SequenceNumber': '25100000000012761275307', 'SizeBytes': 110, 'StreamViewType': 'NEW_IMAGE'}, 'eventSourceARN': 'arn:aws:dynamodb:us-east-1:370808428405:table/user/stream/2021-06-06T18:39:19.798'}]}

def add_item(ph_no):
    return 'done'

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] in 'INSERT' or 'MODIFY':
            new_image = {k: deserialize(v) for k, v in record['dynamodb']['NewImage'].items()}
            ph_no = new_image['PhoneNo']
            add_item(ph_no)
    return 'OK'

