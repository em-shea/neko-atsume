import io
import os
import csv
import json
import boto3
from random import randint

cat_list = []

def lambda_handler(event, context):

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response.decode("utf-8"))
    reader = csv.DictReader(stream)

    for row in reader:
        # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
        cat_image = row['CatImage']
        memento_image = row['MementoImage']
        cat_image = "https://neko-atsume.s3.amazonaws.com/img/" + remove_spaces(cat_image)
        memento_image = "https://neko-atsume.s3.amazonaws.com/img/" + remove_spaces(memento_image)
        cat_list.append(row)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            # 'Access-Control-Allow-Origin': os.environ['DomainName'],
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(cat_list)
    }

def remove_spaces(file_name):

    for letter in file_name:
        if letter = " ":
            letter = "+"

    return file_name