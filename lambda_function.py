import json
from intents.Intent import Intent
from intents.ListEC2Intent import ListEC2Intent
from intents.IntentType import IntentType

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': 400 if err else 200,
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def get_intent(event):
    intent = event['queryResult']['intent']['name']
    intent = intent.rsplit('/', 1)[1]
    return intent


def lambda_handler(event, context):
    event = json.loads(event['body'])

    intent_type = get_intent(event)
    intent = Intent(event)

    if intent_type == IntentType.LIST_EC2.value:
        print('oi')
        intent = ListEC2Intent(event)

    return_json = intent.run()

    return respond(None, return_json)
