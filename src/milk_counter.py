import botocore.exceptions
from common import render_response, user_table
import json


def update_count(phone_number, milk_quantity):
    try:
        response = user_table.update_item(
            Key={
                'PhoneNo': phone_number
            },
            UpdateExpression="set MilkBalance  = MilkBalance + :val",
            ConditionExpression=f"attribute_exists(PhoneNo)",
            ExpressionAttributeValues={
                ':val': milk_quantity
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)
        current_count = int(response['Attributes']['MilkBalance'])
        previous_count = current_count - milk_quantity
        resp = {'status_code': 201, 'message': {'Response': 'Count updated', 'PreviousQuantity': previous_count,
                                                'CurrentQuantity': current_count}}
    except botocore.exceptions.ClientError as e:
        print(e.response)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            resp = {'status_code': 400,
                    'message': {'Response': f"User don't exist with phone number: {phone_number}"}}
        else:
            resp = {'status_code': 500, 'message': {'Response': 'Please reach out to Support'}}
    return resp


def lambda_handler(event, context):
    print(event)
    if ('body' not in event or
            event['httpMethod'] != 'POST'):
        return render_response({'status_code': 400, 'message': {'Response': 'Bad Request'}})

    data = json.loads(event['body'])
    if 'PhoneNo' in data and 'MilkBalance' in data:
        phone_number = data.get('PhoneNo')
        milk_quantity = data.get('MilkBalance')
        resp = update_count(phone_number, milk_quantity)
    else:
        resp = {'status_code': 400, 'message': {'Response': 'Missing PhoneNo and MilkBalance'}}

    return render_response(resp)
