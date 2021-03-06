import boto3
from boto3.dynamodb.conditions import Key
import os
import tweepy
from datetime import date

# environment parameters
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
NUM_POEMS = int(os.environ.get("NUM_POEMS")) # you could query this from the table but to save cost we hard-code it
DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# boto3 resources
dynamodb = boto3.resource('dynamodb')

# clients
twitter_client = tweepy.Client(consumer_key=CONSUMER_KEY,
                        consumer_secret=CONSUMER_SECRET,
                        access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_TOKEN_SECRET)


def get_poem_number_by_date(query_date=date.today()):
    date_0 = date(2000, 1, 1)
    date_1 = query_date
    delta = date_1 - date_0
    poem_num = delta.days % NUM_POEMS + 1
    return poem_num

def handler(event,context):
    """
    Read the event generated by S3.
    get s3 bucket name and object name from event.
    Read the object from s3.
    convert to dict object
    add dict item to dynamo db table.
    """

    # get number of today's poem
    poem_num = get_poem_number_by_date(date.today())

    # get poem from table 
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)    
    ddb_response = table.query(
        KeyConditionExpression=Key('Number').eq(poem_num)
    )
    poem_record = ddb_response.get('Items')[0]
    poem = poem_record.get('Translation')

    # post poem
    response = twitter_client.create_tweet(text=poem)

    return response