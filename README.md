# aws-demo-textract

This demo is targeted toward SAs presenting to their customers. Any overview slides used at the beginning can be tailored to the specific case. Initial version will cover Detecting and Analyzing Text for Single-paged documents using Textract's Synchronous Operations.

Future plans are to add the use of VPC endpoints, as many of our customers prefer that path. A Part II will be added to include themodifications and additional components to support Multipage documents using the Asynchronous Operations.

The overall architecture follows the [AWS Sample Code for Large scale document processing with Amazon Textract](https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing), with this tailored for a demo to fit within a 1-2 hour customer call versus a longer workshop format.

## Architecture
*from above sample repo*<br />
![Architecture Diagram](https://github.com/aws-samples/amazon-textract-serverless-large-scale-document-processing/blob/master/arch.png)



## Demo Build Process
- Create the S3 bucket
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
