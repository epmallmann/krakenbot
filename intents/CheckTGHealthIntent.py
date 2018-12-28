from intents.Intent import Intent
import boto3


class CheckTGHealthIntent(Intent):

    arns = {
        'Common': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/HTTPS/7c29c4cd637fbead',
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/HTTP/c606907a4568df84'
        ],
        'Ticket': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/Ticket/77a0bcf1beb6445c',
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/Ticket-HTTP/c003f76329e43875'
        ],
        'Isolated': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/Isolated/ecdea078a417b86d'
        ],
        'WebSocket': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/WebSockets/937af4de7d081546'
        ],
        'Intensive': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/CPU-Intensive/7628cb1b67d1459e'
        ],
        'Dashboard': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/Dashboard/208adb6243b79ecf'
        ]
    }

    def run(self):
        ec2_target_type = self.event['queryResult']['parameters']['EC2TargetType']

        elb = boto3.client('elbv2')
        ec2 = boto3.client('ec2')

        arns_of_target = self.arns[ec2_target_type]

        cards = []

        for arn in arns_of_target:
            response = elb.describe_target_health(TargetGroupArn=arn)
            healths = response['TargetHealthDescriptions']
            for target in healths:
                instance_id = target['Target']['Id']
                instance_response = ec2.describe_instances(InstanceIds=[instance_id])

                tags = instance_response['Reservations'][0]['Instances'][0]['Tags']
                instance_name = ''
                for tag in tags:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']

                port = target['HealthCheckPort']

                cards.append({'card': {
                    'title': port + ' / ' + instance_id + ' / ' + instance_name,
                    'subtitle': target['TargetHealth']['State']}})

        return_json = {'fulfillmentMessages': cards}
        return return_json
