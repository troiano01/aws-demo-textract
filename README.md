#aws-demo-textract

##Create an SQS Queue for S3 Uploads
textractDemoS3UploadQ for .png files in the 'uploads' prefix

##Create an S3 Bucket
troiano-demo-textract
create a folder 'uploads/'
create an event notification under the 'properties' tab called 'textractDemoS3UploadComplete'
- folder = uploads
- events = Put and Multipart upload completed
- Destination = textractDemoS3UploadQ

'''
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
'''

Show DetectDocumentText output

python -m pip install —upgrade pip

pip3 install boto3 --upgrade —target python/

python -m pip install amazon-textract-response-parser --upgrade --target python
python -m pip install amazon-textract-response-parser --upgrade --target python

zip boto3-layer.zip -r python
