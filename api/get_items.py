import io
import os
import csv
import json
import boto3

def list_cats_handler(event, context):

    object_type = "cat"

    status_code, cat_list = read_s3_data(object_type)

    response = create_response(status_code, cat_list)

    return response

def get_cat_by_id_handler(event, context):

    object_type = "cat"

    cat_id = event['pathParameters']['id']

    cat_id = cat_id.replace('-', ' ')

    status_code, cat_found_response = read_s3_data(object_type, cat_id)

    response = create_response(status_code, cat_found_response)

    return response

def list_goodies_handler(event, context):

    object_type = "goody"

    status_code, goodies_list = read_s3_data(object_type)

    response = create_response(status_code, goodies_list)

    return response

def get_goodies_by_id_handler(event, context):

    object_type = "goody"

    goody_id = event['pathParameters']['id']

    goody_id = goody_id.replace('-', ' ')

    status_code, goody_found_response = read_s3_data(object_type, goody_id)

    response = create_response(status_code, goody_found_response)

    return response

def read_s3_data(object_type, item_id=None):

    if object_type == "cat":
        s3_bucket_name = os.environ['CATS_BUCKET_NAME']
        s3_bucket_key = os.environ['CATS_BUCKET_KEY']
        id_row = 'CatId'
        name_row = 'CatName'
        image_transform_function = cat_image_transform
        error_message = "Cat not found. Request a valid cat name (not case sensitive) or cat id (between 1-66)."

    else:
        s3_bucket_name = os.environ['GOODIES_BUCKET_NAME']
        s3_bucket_key = os.environ['GOODIES_BUCKET_KEY']
        id_row = 'GoodyId'
        name_row = 'GoodyName'
        image_transform_function = goody_image_transform
        error_message = "Goody not found. Request a valid goody name (not case sensitive) or goody id (between 1-185)."

    s3 = boto3.client('s3')

    csv_file = s3.get_object(Bucket=s3_bucket_name, Key=s3_bucket_key)
    csv_response = csv_file['Body'].read()
    stream = io.StringIO(csv_response.decode("utf-8"))
    reader = csv.DictReader(stream)

    item_list = []
    for row in reader:
        if item_id is None or row[id_row] == item_id or row[name_row].lower() == item_id.lower():
            row = image_transform_function(row)
            item_list.append(row)
    if item_id is None:
        return 200, item_list
    else:
        if len(item_list) == 1:
            return 200, item_list[0]
        else:
            error_message = {"error":error_message}
            return 404, error_message 

def cat_image_transform(row):
    # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
    row['CatImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['CatImage'].replace(" ", "+")
    row['MementoImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['MementoImage'].replace(" ", "+")
    return row

def goody_image_transform(row):
    # Example image link: https://neko-atsume.s3.amazonaws.com/img/Aluminum+Pins.jpg
    row['GoodyImage'] = "https://neko-atsume.s3.amazonaws.com/img/" + row['GoodyImage'].replace(" ", "+")
    return row

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