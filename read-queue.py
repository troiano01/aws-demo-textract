import boto3
import json

# The AWS Profile contains the region and output format (in .aws/config) and the 
# access and secret keys (in .aws/credentials)
session = boto3.session.Session( profile_name = 'aws-main' )

# Get the service resource
sqs = session.resource( 'sqs' )

# Get the queue
queue = sqs.get_queue_by_name(QueueName = 'textractDemoQueue')

# Process messages by printing out body and optional author name
messages = queue.receive_messages()

for message in messages:
    msg = json.loads(message.body)
    print(msg['Message'])
    message.delete()
