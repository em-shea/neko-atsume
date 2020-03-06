import io
import os
import csv
import json
import boto3

def list_cats_handler(event, context):

    status_code, cat_list = read_s3_data(list_cats)

    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            # 'Access-Control-Allow-Origin': os.environ['DomainName'],
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(cat_list)
    }

def get_cat_by_id_handler(event, context):

    cat_id = event['pathParameters']['id']

    status_code, response = read_s3_data(get_cat_by_id, cat_id)

    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            # 'Access-Control-Allow-Origin': os.environ['DomainName'],
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response)
    }

#cat_id only passed for get_cat_by_id type requests
def read_s3_data(request_type, cat_id):

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=os.environ['WORDS_BUCKET_NAME'], Key=os.environ['WORDS_BUCKET_KEY'])
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response.decode("utf-8"))
    reader = csv.DictReader(stream)

    if request_type == list_cats:
        cat_list = []
        for row in reader:
            # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
            row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
            row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
            cat_list.append(row)
        # return status code and API results
        return 200, cat_list
    
    if request_type == get_cat_by_id:
        for row in reader:
            if row['CatId'] == cat_id:
                # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
                row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
                row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
                # return status code and API results
                return 200, row
        # if no cats found by id, return error code
        error_message = {"error":"Cat not found. Enter an id between 1-66."}
        return 404, error_message
