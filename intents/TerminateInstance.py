from intents.Intent import Intent
import boto3
import os


class TerminateInstance(Intent):

    def run(self):
        slack_user_id = self.event['originalDetectIntentRequest']['payload']['data']['user']

        allowed_users = os.environ['allowed_slack_users'].split(",")
        if slack_user_id not in allowed_users:
            return {'fulfillmentText': 'Usuário não autorizado!'}

        ec2_target_type = self.event['queryResult']['parameters']['EC2TargetType']
        urgency = self.event['queryResult']['parameters']['urgency']
        qty = self.event['queryResult']['parameters']['qty']

        if not qty or qty == 0:
            qty = 1

        group_name = self.get_group_name(ec2_target_type, urgency)

        client_asg = boto3.client('autoscaling')

        auto_scaling_groups = client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])

        print(auto_scaling_groups)

        if len(auto_scaling_groups['AutoScalingGroups']) == 0:
            return {'fulfillmentText': 'Grupo {} não encontrado!'.format(group_name)}

        original_desired_capacity = auto_scaling_groups['AutoScalingGroups'][0]['DesiredCapacity']
        desired_capacity = int(original_desired_capacity) - int(qty)

        if desired_capacity < 0:
            desired_capacity = 0

#        client_asg.set_desired_capacity(AutoScalingGroupName=group_name, DesiredCapacity=desired_capacity)

        msg_capacity = 'Desired capacity alterado de {} para {}.'\
            .format(str(original_desired_capacity), str(desired_capacity))
        msg_group = 'Grupo alterado: ' + group_name

        return_json = {'fulfillmentMessages': [{'text': {'text': [msg_capacity]}}, {'text': {'text': [msg_group]}}]}
        return return_json

    def get_group_name(self, ec2_target_type, urgency):
        group_name = ec2_target_type
        if urgency:
            group_name += '-Emergency'
        return group_name
