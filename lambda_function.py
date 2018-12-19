import json
from intents.Intent import Intent
from intents.ListEC2Intent import ListEC2Intent
from intents.GetLogIntent import GetLogIntent
from intents.GenerateS3UrlIntent import GenerateS3UrlIntent
from intents.CheckTGHealthIntent import CheckTGHealthIntent
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
        intent = ListEC2Intent(event)
    elif intent_type == IntentType.GET_LOG.value:
        intent = GetLogIntent(event)
    elif intent_type == IntentType.S3_URL.value:
        intent = GenerateS3UrlIntent(event)
    elif intent_type == IntentType.TG_HEALTH.value:
        intent = CheckTGHealthIntent(event)

    return_json = intent.run()

    return respond(None, return_json)
