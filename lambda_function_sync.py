import json
import boto3
import os
import urllib.parse
from datetime import datetime
from trp import Document

def lambda_handler(event, context):
    
    for record in event['Records']:
        
        # Get the bucket and filename (key) from the event and set the output filenames
        msg = json.loads(record['body'])
        eventBucket = msg['Records'][0]['s3']['bucket']['name']
        eventKey = urllib.parse.unquote_plus(msg['Records'][0]['s3']['object']['key'])
        uploadedFullFilename = os.path.basename(eventKey)
        uploadedFilename = os.path.splitext(uploadedFullFilename)[0]
        jsonOutputPrefix = "processed/json/"
        summaryOutputPrefix = "processed/summaries/"
        outputJsonFile1 = jsonOutputPrefix + uploadedFilename + ".json"
        outputJsonFile2 = summaryOutputPrefix + uploadedFilename + ".txt"
        
        # print the bucket and filename to the application log
        print("Bucket: " + eventBucket)
        print("Path & Filename: " + eventKey)
        print("JSON output in " + outputJsonFile1)
        print("Summary output in " + outputJsonFile2)
        
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
                parsedOutput = parsedOutput + field.key.text + ', ' + field.value.text + '\n'
            parsedOutput = parsedOutput + '\n'
    
        # Print to the application log
        print(parsedOutput)
        
        # Write JSON response to a file in s3
        json2s3(json.dumps(response['Blocks']), eventBucket, outputJsonFile1)
        json2s3(json.dumps(parsedOutput), eventBucket, outputJsonFile2)
        
        # Post notification that the file processing is completed.
        completionTime = datetime.now()
        snsMessage = completionTime.strftime("%d/%m/%Y %H:%M:%S") + ": File " + uploadedFullFilename + " has been processed."
        print(snsMessage)
        response = textract2Sns(snsMessage)
        
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
        return {'statusCode': 200}
        
    except Exception as e:
        print(e)
        return(e)
