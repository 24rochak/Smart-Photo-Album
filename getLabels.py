import boto3

def listItems(bucketname,foldername):
    import boto3 
    s3 = boto3.client("s3")
    response = s3.list_objects(
            Bucket=bucketname,
            Prefix ='photos/',
            MaxKeys=100 )

    contents = response['Contents']
    imnames = [item['Key'] for item in contents[1:]]
    return imnames

def getLabel(bucketname, im):
    client=boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucketname,'Name':im}},
        MaxLabels=10)
    labels = set(label['Name'] for label in response['Labels'])
    return labels

def getAllLabels(bucketname,imnames):
    labels = set()
    for im in imnames:
        tempLabels = getLabel(bucketname,im)
        print("Temp Lables: ",tempLabels)
        labels = labels.union(tempLabels)
    return labels

bucketname = 'photo-s3'
imnames = listItems(bucketname,None)
labels = getAllLabels(bucketname,imnames[:1])
print(list(labels))