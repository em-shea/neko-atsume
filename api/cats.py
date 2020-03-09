import io
import os
import csv
import json
import boto3

def list_cats_handler(event, context):

    status_code, cat_list = read_s3_data()

    response = create_response(status_code, cat_list)

    return response

def get_cat_by_id_handler(event, context):

    cat_id = event['pathParameters']['id']

    status_code, cat_found_response = read_s3_data(cat_id)

    response = create_response(status_code, cat_found_response)

    return response

#cat_id only passed for get_cat_by_id type requests
def read_s3_data(cat_id=None):

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response.decode("utf-8"))
    reader = csv.DictReader(stream)

    cat_list = []
    for row in reader:
        if cat_id is None or row['CatId'] == cat_id or row['CatName'].lower() == cat_id.lower():
            # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
            row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
            row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
            cat_list.append(row)
    if cat_id is None:
        return 200, cat_list
    else:
        if len(cat_list) == 1:
            return 200, cat_list[0]
        else:
            error_message = {"error":"Cat not found. Request a valid cat name or cat id (between 1-66)."}
            return 404, error_message 

def create_response(status_code, response_body):

    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            # 'Access-Control-Allow-Origin': os.environ['DomainName'],
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response_body)
    }