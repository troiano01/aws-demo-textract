import boto3

# AWS Profiles contain the region and output format (in .aws/config) and the 
# access and secret keys (in .aws/credentials)
session = boto3.session.Session( profile_name = 'aws-demo-main' )

# Define the S3 rersource
s3 = session.resource( 's3' )

# File to upload
demoFile = 'demofiles/employmentapp.png'

# Bucket to which the file will be uploaded
demoBucket = 'troiano-demo-textract2'

# Key includes the filename and s3 prefixes (folders) without a preceeding '/'
demoKey1 = 'uploads/employmentapp1.png'

s3.meta.client.upload_file(
    Filename = demoFile,
    Bucket = demoBucket,
    Key = demoKey1
)
