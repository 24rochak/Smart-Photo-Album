import json
import urllib3
import boto3
from botocore.exceptions import ClientError
import os

'''
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import scan
'''

global endpoint
#endpoint = "vpc-photos-iyqoulxe2cmgeprfim4lcb47aq.us-east-1.es.amazonaws.com"
endpoint = "https://"+os.environ['ESENDPOINT']

def listItems(bucketname,foldername):
    s3 = boto3.client("s3")
    try:
        response = s3.list_objects(
                Bucket=bucketname,
                Prefix =foldername+'/',
                MaxKeys=100)
    except ClientError as e:
        return e

    contents = response['Contents']
    imnames = [item['Key'] for item in contents[1:]]
    return imnames

def getLabels(bucketname, im):
    client=boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucketname,'Name':im}},
        MaxLabels=10)
    labels = set(label['Name'].lower() for label in response['Labels'])
    return labels

'''
def countElements():
    session = boto3.session.Session()
    credentials = session.get_credentials()
    service = 'es'
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, session.region_name, 'es', 
                        session_token=credentials.token)
    es = Elasticsearch(endpoint,http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    return es.count()['count']
    
def clearES():
    session = boto3.session.Session()
    credentials = session.get_credentials()
    service = 'es'
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, session.region_name, 'es', 
                        session_token=credentials.token)
    es = Elasticsearch(endpoint,http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    es_response = scan(es,index='photo',doc_type='_doc',query={"query": { "match_all" : {}}})
    for item in es_response:
        es.delete(index='photo',doc_type='_doc',id=item['_id'])
        
    count = countElements()
    if count!=0:
        print("Not deleted successfully. Count is: ",count)
        return False
    else:
        print("Deleted successfully. Count is: ",count)
        return True
'''


def init():
    http = urllib3.PoolManager()
    indexURL = endpoint+"/photo"
    item={"mappings": {
                        "properties": {
                            "objectkey": {"type": "text", "index": False},
                            "labels": {"type": "keyword"},
                                        }
                                }
    }
    encoded_data = json.dumps(item).encode('utf-8')
    result = http.request('PUT', indexURL, body=encoded_data,headers={'Content-Type': 'application/json'}).data
    response = json.loads(result.decode('utf-8'))
    if response['status']==400:
        return response
    else:
        print("Error creating Index")
        return None

def indexImages():
    foldername = 'photos'
    bucketname = 'photo-s3'
    imnames = listItems(bucketname, foldername)
    
    http = urllib3.PoolManager()
    indexURL = endpoint+"/photo/_doc"
    
    allLabels = set()
    for im in imnames:
        labels = getLabels(bucketname,im)
        allLabels = allLabels.union(labels)
        item = {}
        item['objectkey'] = im
        item['labels'] = list(labels)
        encoded_data = json.dumps(item).encode('utf-8')
        result = http.request('POST', indexURL, body=encoded_data,headers={'Content-Type': 'application/json'}).data
        response = json.loads(result.decode('utf-8'))
    return allLabels, None

def lambda_handler(event, context):
    # TODO implement
    response = init()
    if response is None:
        print("Error creating index mappings")
        return
    
    allLabels, err = indexImages()
    #All Labels:  {'produce', 'rug', 'water', 'parrot', 'school', 'petal', 'couch', 'human', 'lawn', 'veterinarian', 'vehicle', 'finch', 'sycamore', 'plant', 'room', 'indoors', 'blossom', 'asteraceae', 'beak', 'sunflower', 'tire', 'sports car', 'person', 'wheel', 'bird', 'machine', 'sea', 'pizza', 'grass', 'classroom', 'jar', 'wood', 'macaw', 'park', 'potted plant', 'car', 'daisies', 'tree trunk', 'lily', 'transportation', 'flower', 'anthus', 'field', 'sparrow', 'animal', 'alloy wheel', 'nature', 'outdoors', 'car wheel', 'vegetable', 'flooring', 'hot dog', 'oak', 'clothing', 'food', 'vase', 'spoke', 'vegetation', 'pottery', 'doctor', 'interior design', 'shorts', 'garden', 'pond lily', 'tree', 'daisy', 'scenery'}
    if err is None:
        print("Indexed Images successfully")
    print("All Labels: ",allLabels)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
