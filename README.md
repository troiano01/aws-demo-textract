# aws-demo-textract

This demo is targeted toward SAs presenting to their customers. Any overview slides used at the beginning can be tailored to the specific case. Initial version will cover Detecting and Analyzing Text for Single-paged documents using Textract's Synchronous Operations.

Future plans are to add the use of VPC endpoints, as many of our customers prefer that path. A Part II will be added to include the modifications and additional components to support Multipage documents using the Asynchronous Operations. DynamoDB can be added to store document metadata, both in its incoming and processed states.

The overall architecture follows the [AWS Sample Code for Large scale document processing with Amazon Textract](https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing), and is tailored for a demo to fit within a 1-2 hour customer call versus a longer workshop format. The Sample Code repository has a more complete solution build customers can use for reference. Where it uses AWS CDK to deploy, this demo walks through building the base components using the console. The code provided below is for demonstative purposes only and does not include a production-ready user experience and error handling.

## Architecture
**from the above sample GitHub repository*<br />
![Architecture Diagram](https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing/blob/master/arch.png)

## Architecture Components and Workflow
1. The process starts with a sample file uploaded to S3. For this we use a simple python script.
2. Once uploaded, the S3 Bucket uses an Event Notification to send a message to an Amazon SQS queue.
3. This SQS queue is set as a trigger for a Lambda function...
4. The Lambda function obtains the S3 Bucket and file from the SQS queue message and calls Textract's analyze_document API
5. It next calls the Document function from a [Textract Response Parser](https://github.com/aws-samples/amazon-textract-response-parser) (referenced in the [Textract documentation](https://docs.aws.amazon.com/textract/latest/dg/other-examples.html)) that processes the Textract output, returning it as a custome Document object that contains pages as Python Lists. These lists make it easier to parse the document into a readable format. 
6. The function parses the output into a summary and publishes ...
7. Finally it saves the output and summary in two files...
8. A simple python script reads the completion message from the SQS queue. A customer's application can poll this queue for completed documents or use one or more of SNS' protocols to push completion notification.
9. If DynamoDB is used for document metadata, the completion state and any relevant data can be updated.

## Demo Build Process
- Create the S3 bucket

## S3 Upload
```
import boto3

# AWS Profiles contain the region and output format (in .aws/config) and the 
# access and secret keys (in .aws/credentials)
session = boto3.session.Session( profile_name = 'aws-main' )

# Define the S3 rersource
s3 = session.resource( 's3' )

# File to upload
demoFile = 'demofiles/employmentapp.png'

# Bucket to which the file will be uploaded
demoBucket = 'troiano-demo-textract'

# Key includes the filename and s3 prefixes (folders) without a preceeding '/'
demoKey1 = 'uploads/employmentapp1.png'

s3.meta.client.upload_file(
    Filename = demoFile,
    Bucket = demoBucket,
    Key = demoKey1
)
```

## Create an SQS Queue for S3 Uploads
1. textractDemoS3UploadQ for .png files in the 'uploads' prefix
2. Set the visibility timeout to 60 sec (10x the function timeout, from below)

Configuring a queue as an event source


## Create an S3 Bucket
1. troiano-demo-textract
2. create a folder 'uploads'
3. Note the ARN

#### Add access to SQS for the S3 Bucket
(Needs to be added before the Event Notification step below or S3 will not be able to validate its access)

```
{
 "Version": "2012-10-17",
 "Statement": [
  {
   "Sid": "s3-upload-access",
   "Effect": "Allow",
   "Principal": {
     "Service": "s3.amazonaws.com"  
   },
   "Action": [
    "SQS:SendMessage"
   ],
   "Resource": "arn:aws:sqs:Region:account-id:queue-name",
   "Condition": {
      "ArnLike": { "aws:SourceArn": "arn:aws:s3:*:*:awsexamplebucket1" }
   }
  }
 ]
}
```
#### Add the S3 Event Notification
1. create an event notification under the 'properties' tab called 'textractDemoS3UploadComplete'
   - folder = uploads
   - events = Put and Multipart upload completed
   - Destination = textractDemoS3UploadQ

#### Async Function
1. Create a new function called textractDemoAsync
2. Runtime = Python 3.7
3. Permissions = Create a new role
   <br />(we'll update the roles permissions later)
4. Paste the code (lambda_function_async.py)
5. Configuration tab, choose General configuration and set the timeout to 10 sec
6. 

6. Update the role permissions by choosing Permissions from the list under the Configuration tab
   - Add AWSLambdaSQSQueueExecutionRole
   - Add AWSLambdaBasicExecutionRole 
   - Remove any others

Add the SQS Event Trigger
- Choose the Q
- Leave the defaults and uncheck Enable trigger (will enable it later)

Create CloudWatch Event to schedule the Lambda function to pull from SQS and disable it





Later Updates
- Function in VPC with Endpoints
- Dead Letter Queue (maxReceiveCount to at least 5)



Show DetectDocumentText output

python -m pip install —upgrade pip

pip3 install boto3 --upgrade —target python/

python -m pip install amazon-textract-response-parser --upgrade --target python
python -m pip install amazon-textract-response-parser --upgrade --target python

zip boto3-layer.zip -r python
