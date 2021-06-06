import botocore.exceptions
from common import render_response, user_table, table_name
import json


def add_user(data):
    params = {
        'PhoneNo': data.get('PhoneNo'),
        'FirstName': str(data.get('FirstName')).lower(),
        'LastName': str(data.get('LastName')).lower(),
        'Address': data.get('Address'),
        'Landmark': data.get('Landmark'),
        'PlusCode': data.get('PlusCode', '')
    }
    params.update({'cache': 'account'})
    try:
        response = user_table.put_item(
            TableName=table_name,
            Item=params,
            ConditionExpression=f"attribute_not_exists(PhoneNo)",
        )
        print(response)
        resp = {'status_code': 201, 'message': {'Response': 'User created'}}
    except botocore.exceptions.ClientError as e:
        print(e.response)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            resp = {'status_code': 400,
                    'message': {'Response': 'User already exist, to edit an user please use edit service.'}}
        else:
            resp = {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}
    return resp


def lambda_handler(event, context):
    print(event)
    if ('body' not in event or
            event['httpMethod'] != 'POST'):
        return render_response({'status_code': 400, 'message': {'Response': 'Bad Request'}})

    data = json.loads(event['body'])
    resp = add_user(data)
    return render_response(resp)
