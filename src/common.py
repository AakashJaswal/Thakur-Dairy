import json
import boto3
import os

table_name = os.environ.get('TABLE', 'user')
dynamo = boto3.resource('dynamodb')
user_table = dynamo.Table(table_name)

render_response = lambda resp: {
    'statusCode': resp['status_code'],
    'headers': {
        'Content-Type': 'application/json'
    },
    'body': json.dumps(resp['message'])
}
