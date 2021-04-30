import json
import boto3
import urllib.parse
from trp import Document

def lambda_handler(event, context):
    
    for record in event['Records']:
        
        # Get the bucket and filename (key) from the event
        msg = json.loads(record['body'])
        eventBucket = msg['Records'][0]['s3']['bucket']['name']
        eventKey = urllib.parse.unquote_plus(msg['Records'][0]['s3']['object']['key'])
        
        # print the bucket and filename to the log
        print("Bucket: " + eventBucket)
        print("Path & Filename: " + eventKey)
        
        # Create the Textract session and call analyze_document()
        client = boto3.client('textract')
        response = client.analyze_document(
            Document = {'S3Object': {'Bucket': eventBucket, 'Name': eventKey}},
            FeatureTypes = ['TABLES','FORMS']
        )
        
        # Parse JSON response from Textract using amazon-textract-response-parser
        # https://github.com/aws-samples/amazon-textract-response-parser
        doc = Document(response)
        
        parsedOutput = ''
    
        # Iterate over elements in the document (print output appears in the application log)
        for page in doc.pages:
            
            # Print lines and words
            for line in page.lines:
                parsedOutput = parsedOutput + '-\nline: ' + line.text + ' (' + str(line.confidence) + ')\n'
                parsedOutput = parsedOutput + '-----------------------------------------------------\n'
                for word in line.words:
                    parsedOutput = parsedOutput + 'word: ' + word.text + ' (' + str(word.confidence) + ')\n'
        
            # Print tables
            for table in page.tables:
                parsedOutput = parsedOutput + '-\ntable\n'
                parsedOutput = parsedOutput + '-----------------------------------------------------\n'
                for r, row in enumerate(table.rows):
                    parsedOutput = parsedOutput + '\n'
                    for c, cell in enumerate(row.cells):
                        parsedOutput = parsedOutput + cell.text.replace(',', '').strip() + ','
                parsedOutput = parsedOutput + '\n'
        
            # Print fields
            parsedOutput = parsedOutput + '-\nfields\n'
            parsedOutput = parsedOutput + '-----------------------------------------------------\n'
            for field in page.form.fields:
                parsedOutput = parsedOutput + field.key.text + ': ' + field.value.text + '\n'
            parsedOutput = parsedOutput + '\n'
    
        print(parsedOutput)
        
        # Write JSON response to a file in s3
        #json2s3(json.dumps(response['Blocks']), eventBucket, outputJsonFile1)
        #json2s3(json.dumps(response), eventBucket, outputJsonFile2)
        
        #response = textract2Sns(json.dumps(response['Blocks']))
        response = textract2Sns(parsedOutput)
        
        return {'statusCode': 200}
        
def json2s3(output_body, output_bucket, output_file):

    s3 = boto3.client('s3')
    s3.put_object(
        Body = output_body,
        Bucket = output_bucket,
        Key = output_file
    )

    return {'statusCode': 200}

def textract2Sns(output_body):

    try:
        sns = boto3.client('sns')
        response = sns.publish(
            TopicArn = "arn:aws:sns:us-east-1:089091079446:textractSnsDemo",    
            Message = output_body 
        )
        print(response)
        return {'statusCode': 200}
        
    except Exception as e:
        print(e)
        return(e)
    
        return {'statusCode': 200} 
