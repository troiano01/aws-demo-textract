import boto3
import json

# The AWS Profile contains the region and output format (in .aws/config) and the 
# access and secret keys (in .aws/credentials)
session = boto3.session.Session( profile_name = 'aws-demo-main' )

# Get the service resource
sqs = session.resource( 'sqs' )

# Get the queue
queue = sqs.get_queue_by_name(QueueName = 'textractDemoQ')

# Process messages by printing out body and optional author name
try:
    messages = queue.receive_messages()
except Exception as e:
    print(e)

for message in messages:
    msg = json.loads(message.body)
    print(msg['Message'])
    message.delete()
