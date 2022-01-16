import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")

def handler(event,context):
    """
    Read the object from Lambda local storage
    Convert to dict object
    Add dict data to DynamoDB table.
    """
    # read json object as dict
    artist_config_path = os.path.join(os.path.dirname(__file__),"data/thirukkural.json")
    with open(artist_config_path) as f:
        dict_poems = json.load(f)
        
    # add dict items to DynamoDB table
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    for kural in dict_poems['kural']:
        table.put_item(Item=kural)

    return "Poems inserted succesfully"