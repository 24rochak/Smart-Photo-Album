import boto3

def putSlot(labels, checksum):
    client = boto3.client('lex-models')
    vals = []
    for label in labels:
        item = {}
        item['value'] = label.lower()
        vals.append(item)
    response = client.put_slot_type(name='Keyword_one',enumerationValues=vals, 
                                    valueSelectionStrategy='ORIGINAL_VALUE',
                                    checksum=checksum)
    print(response)

def getSlotValues(slotName):
    client = boto3.client('lex-models')
    response = client.get_slot_type(
        version='$LATEST',
        name=slotName,
    )
    vals = [item['value'] for item in response['enumerationValues']]
    checksum = response['checksum']
    return vals, checksum

def getBot(botname, version):
    client = boto3.client('lex-models')
    response = client.get_bot(name=botname, versionOrAlias=version)
    return response

# labels, checksum = getSlotValues('Keyword_one')
# print(labels)
# AllLabels = {'produce', 'rug', 'water', 'parrot', 'school', 'petal', 'couch', 'human', 'lawn', 'veterinarian', 'vehicle', 'finch', 'sycamore', 'plant', 'room', 'indoors', 'blossom', 'asteraceae', 'beak', 'sunflower', 'tire', 'sports car', 'person', 'wheel', 'bird', 'machine', 'sea', 'pizza', 'grass', 'classroom', 'jar', 'wood', 'macaw', 'park', 'potted plant', 'car', 'daisies', 'tree trunk', 'lily', 'transportation', 'flower', 'anthus', 'field', 'sparrow', 'animal', 'alloy wheel', 'nature', 'outdoors', 'car wheel', 'vegetable', 'flooring', 'hot dog', 'oak', 'clothing', 'food', 'vase', 'spoke', 'vegetation', 'pottery', 'doctor', 'interior design', 'shorts', 'garden', 'pond lily', 'tree', 'daisy', 'scenery'}
# putSlot(allLabels,checksum)

bot = getBot('SearchBot', 'production')
print(bot)