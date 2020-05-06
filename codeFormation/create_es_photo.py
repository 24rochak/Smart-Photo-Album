import json
import boto3
import urllib3
import os
#from elasticsearch import Elasticsearch, RequestsHttpConnection
#from requests_aws4auth import AWS4Auth

global endpoint
#endpoint = "vpc-photos-iyqoulxe2cmgeprfim4lcb47aq.us-east-1.es.amazonaws.com"
endpoint = "https://"+os.environ['ESENDPOINT']

INDEX = "photo"
ES_SEARCH_RESULT_SIZE = 10  # the size of the data we expect to be returned from es, set it little to ease the server loading

def detect_labels(photo, bucket):
    reko = boto3.client('rekognition')
    response = reko.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=3)
    return [label['Name'] for label in response['Labels']]

def add_index(photo, labels):
    http = urllib3.PoolManager()
    indexURL = endpoint+"/photo/_doc"
    item = {}
    item['objectkey'] = photo
    item['labels'] = list(labels)
    encoded_data = json.dumps(item).encode('utf-8')
    result = http.request('POST', indexURL, body=encoded_data,headers={'Content-Type': 'application/json'}).data
    response = json.loads(result.decode('utf-8'))
    return response
    
    '''
    session = boto3.session.Session()
    credentials = session.get_credentials()
    service = 'es'
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, session.region_name, 'es', 
                        session_token=credentials.token)
    es = Elasticsearch(ENDPOINT,http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    
    try:
        item = {}
        item['objectkey'] = "photo"
        item['labels'] = [label for label in labels]
        response = es.index(index='photo',body=item)
        return response
    except:
        return None
    '''
    

def lambda_handler(event, context):
    # TODO implement
    print("photo uploaded from s3")
    print(event)
    photo = (event["Records"][0]["s3"]["object"]["key"])
    labels = detect_labels(photo, "photo-s3")
    print("labels detected from Rekognition:",labels)
    resp = add_index(photo, labels)
    print("response from add index to ES:", resp)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
