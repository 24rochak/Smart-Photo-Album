import json
import urllib3
import boto3
import time
import urllib3
import os

global endpoint
#endpoint = "vpc-photos-iyqoulxe2cmgeprfim4lcb47aq.us-east-1.es.amazonaws.com"
endpoint = "https://"+os.environ['ESENDPOINT']

def searchTags(tags):
    http = urllib3.PoolManager()
    searchURL = endpoint+"/photo/_search"
    body = {"query":{"terms" : {"labels":tags}}}
    encoded_data = json.dumps(body).encode('utf-8')
    result = http.request('GET', searchURL, body=encoded_data,headers={'Content-Type': 'application/json'}).data
    response = json.loads(result.decode('utf-8'))
    hits = response['hits']
    count = hits['total']['value']
    if count == 0:
        # No matches
        return []
    filenames = hits['hits'][0]['_source']['objectkey']
    return filenames
    
def getSlots(query):
    client = boto3.client('lex-runtime')
    response = client.post_text(botName='SearchBot', botAlias='production', userId='user1',
                                inputText=query)
    if 'message' in response:
        return None
    return response
    
def lambda_handler(event, context):
    query = 'bird'
    response = getSlots(query)
    if response is None:
        print("Error")
        return {
        'statusCode': 200,
        'body': json.dumps('Input not understood.')
    }
    vals = set(response['slots'].values())
    keywords = set(['photos','pictures','pics','photo','pic','picture',None])
    vals = list(vals-keywords)
    filenames = searchTags(vals)
    print(filenames)
    if len(filenames)==0:
        return {
        'statusCode': 200,
        'body': json.dumps('No matching Photos found in library')
    }
    return {
        'statusCode': 200,
        'body': json.dumps('Photos found')
    }
    
