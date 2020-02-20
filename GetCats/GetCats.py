import io
import os
import csv
import boto3
from random import randint

cat_list = None

def lambda_handler(event, context):

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response)
    reader = csv.DictReader(stream)

    for row in reader:
        print(reader) 