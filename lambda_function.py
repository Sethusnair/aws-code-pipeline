import json
import base64
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user_activity')
s3=boto3.client('s3')
BUCKET='user-analytics-sethu'

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        data_str = payload.decode('utf-8')
        try:
            data = json.loads(data_str)
        except:
            print("Not JSON, raw text:", data_str)
            continue

        table.put_item(Item={
            'userId': data['userId'],
            'action': data['action']
        })

        s3.put_object(
            Bucket=BUCKET,
            Key=f"events/{int(time.time())}.json",
            Body=json.dumps(data)
        )


    return {'statusCode': 200}