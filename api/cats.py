import io
import os
import csv
import json
import boto3

cat_list = []

def list_cats_handler(event, context):

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response.decode("utf-8"))
    reader = csv.DictReader(stream)

    for row in reader:
        # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
        row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
        row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
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

def get_cat_by_id_handler(event, context):

    print("Function event...", event)

    # s3 = boto3.client('s3')

    # csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    # csv_response = csv_file['Body'].read()
    # stream = io.StringIO(csv_response.decode("utf-8"))
    # reader = csv.DictReader(stream)

    # for row in reader:
    #     # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
    #     row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
    #     row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
    #     cat_list.append(row)

    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         'Access-Control-Allow-Methods': 'GET,OPTIONS',
    #         # 'Access-Control-Allow-Origin': os.environ['DomainName'],
    #         'Access-Control-Allow-Origin': '*',
    #     },
    #     'body': json.dumps(cat_list)
    # }