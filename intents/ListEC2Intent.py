from intents.Intent import Intent
import boto3


class ListEC2Intent(Intent):

    def run(self):
        return_json = {}
        cards = []

        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        reservations = response['Reservations']

        for reservation in reservations:
            instances = reservation['Instances']
            for inst in instances:
                name = ''
                for tag in inst['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                cards.append({'card': {'title': inst['InstanceId'], 'subtitle': name}})

        return_json['fulfillmentMessages'] = cards
