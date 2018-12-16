import json
import boto3

print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dump(res),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_regions()
    regions = response['Regions']

    j = {}
    cards = []

    for region in regions:
        card = {}
        # but = [{'text': 'button1', 'postback': 'https://google.com'}]
        # card['card'] = {'title': region['RegionName'], 'subtitle': region['Endpoint']}
        cards.append({'card': {'title': region['RegionName'], 'subtitle': region['Endpoint']}})

    j['fulfillmentMessages'] = cards

    return respond(None, j)
