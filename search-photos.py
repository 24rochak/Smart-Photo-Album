import json

def lambda_handler(event):
    # TODO implement
    inp = event['inputTranscript']
    print(inp)
    keywords = []

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


keywordevent = {'messageVersion': '1.0', 'invocationSource': 'FulfillmentCodeHook', 'userId': 'k3765w7qserhsqotgqm8s1gf3lioirtc', 'sessionAttributes': {}, 'requestAttributes': 'None', 'bot': {'name': 'searchbot', 'alias': '$LATEST', 'version': '$LATEST'}, 'outputDialogMode': 'Text', 'currentIntent': {'name': 'searchIntent', 'slots': {}, 'slotDetails': {}, 'confirmationStatus': 'None'}, 'inputTranscript': 'show me picture trees', 'recentIntentSummaryView': 'None', 'sentimentResponse': 'None'}
searchevent = {'messageVersion': '1.0', 'invocationSource': 'FulfillmentCodeHook', 'userId': 'znywvi1z19vnb2v4s97m6ew7uo6hcub9', 'sessionAttributes': {}, 'requestAttributes': None, 'bot': {'name': 'searchBot', 'alias': '$LATEST', 'version': '$LATEST'}, 'outputDialogMode': 'Text', 'currentIntent': {'name': 'searchIntent', 'slots': {'slotOne': 'bird'}, 'slotDetails': {'slotOne': {'resolutions': [{'value': 'bird'}], 'originalValue': 'bird'}}, 'confirmationStatus': 'None'}, 'inputTranscript': 'bird', 'recentIntentSummaryView': [{'intentName': 'searchIntent', 'checkpointLabel': None, 'slots': {'slotOne': None}, 'confirmationStatus': 'None', 'dialogActionType': 'ElicitSlot', 'fulfillmentState': None, 'slotToElicit': 'slotOne'}], 'sentimentResponse': None}
lambda_handler(keywordevent)