from intents.Intent import Intent
import boto3


class CheckTGHealthIntent(Intent):

    arns = {
        'Common': [
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/HTTP/c606907a4568df84',
            'arn:aws:elasticloadbalancing:us-east-1:452117901698:targetgroup/HTTPS/7c29c4cd637fbead'
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
        ]
    }

    def run(self):
        ec2_target_type = self.event['queryResult']['parameters']['EC2TargetType']

        elb = boto3.client('elbv2')

        arns_of_target = self.arns[ec2_target_type]

        cards = []

        for arn in arns_of_target:
            response = elb.describe_target_health(TargetGroupArn=arn)
            healths = response['TargetHealthDescriptions']
            for target in healths:
                cards.append({'card': {'title': target['Target']['Id'] + ' - ' + target['HealthCheckPort'], 'subtitle': target['TargetHealth']['State']}})

        return_json = {'fulfillmentMessages': cards}
        return return_json
