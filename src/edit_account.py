import botocore.exceptions
from boto3.dynamodb.conditions import Key
from common import render_response, user_table, table_name
import json


def edit_user(data):
    phone_no = data.get('PhoneNo')
    data['FirstName'] = data['FirstName'].lower()
    data['LastName'] = data['LastName'].lower()
    new_data = {}
    try:
        response = user_table.query(
            KeyConditionExpression=Key('PhoneNo').eq(phone_no)
        )
        print(response)
    except botocore.exceptions.ClientError as e:
        print(e.response)
        return {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}

    if response['Count'] != 0:
        old_data = {
            'PhoneNo': response['Items'][0].get('PhoneNo'),
            'FirstName': response['Items'][0].get('FirstName'),
            'LastName': response['Items'][0].get('LastName'),
            'Address': response['Items'][0].get('Address'),
            'Landmark': response['Items'][0].get('Landmark'),
            'PlusCode': response['Items'][0].get('PlusCode', '')
        }
    else:
        return {'status_code': 401, 'message': {'Response': f"User don't exist with phone number: {phone_no}"}}
    new_data.update(data)
    new_data.update({'cache': 'account'})
    try:
        response = user_table.put_item(
            TableName=table_name,
            Item=new_data,
            ConditionExpression=f"attribute_exists(PhoneNo)",
        )
        print(response)
        del new_data['cache']
        resp = {'status_code': 201,
                'message': {'Response': 'User Updated', 'PreviousInfo': old_data, 'CurrentInfo': new_data}}
    except botocore.exceptions.ClientError as e:
        print(e.response)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            resp = {'status_code': 400,
                    'message': {'Response': f"User don't exist with Phone Number: {new_data['PhoneNo']}"}}
        else:
            resp = {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}
    return resp


def lambda_handler(event, context):
    print(event)
    if ('body' not in event or
            event['httpMethod'] != 'POST'):
        return render_response({'status_code': 400, 'message': {'Response': 'Bad Request'}})

    data = json.loads(event['body'])
    resp = edit_user(data)
    return render_response(resp)
