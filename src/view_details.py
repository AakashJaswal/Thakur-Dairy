from common import render_response, user_table
from boto3.dynamodb.conditions import Key
import botocore.exceptions


def search_by_num(phone_no):
    try:
        response = user_table.query(
            KeyConditionExpression=Key('PhoneNo').eq(phone_no)
        )
        print(response)
    except botocore.exceptions.ClientError as e:
        print(e.response)
        return {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}

    if response['Count'] != 0:
        user_data = response['Items'][0]
        del user_data['cache']
        resp = {'status_code': 200, 'message': [user_data]}
    else:
        resp = {'status_code': 401, 'message': {'Response': f"User don't exist with phone number: {phone_no}"}}
    return resp


def search_by_name(prefix):
    scan_kwargs = {
        'FilterExpression': Key('FirstName').begins_with(prefix),
    }
    try:
        response_list = []
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = user_table.scan(**scan_kwargs)
            for item in response.get('Items', []):
                response_list.append(item)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
    except botocore.exceptions.ClientError as e:
        print(e.response)
        return {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}
    for item in response_list:
        del item['cache']
    if response_list:
        resp = {'status_code': 200, 'message': response_list}
    else:
        resp = {'status_code': 401, 'message': {'Response': f"User don't exist with prefix: {prefix}"}}
    print(resp)
    return resp


def lambda_handler(event, context):
    if ('pathParameters' not in event or
            event['httpMethod'] != 'GET'):
        return render_response(400, {'Response': 'Bad Request'})
    if 'name' in event['path']:
        prefix = event['pathParameters']['prefix']
        resp = search_by_name(str(prefix).lower())
    else:
        phone_no = event['pathParameters']['phone_no']
        resp = search_by_num(phone_no)
    print(resp)
    return render_response(resp)
