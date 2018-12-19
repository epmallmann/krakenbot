from intents.Intent import Intent
from datetime import datetime
from dateutil.parser import parse
import boto3


class GetLogIntent(Intent):

    def run(self):
        instance_id = self.event['queryResult']['parameters']['InstanceId']
        date_time_param = self.event['queryResult']['parameters']['date-time']

        if date_time_param != '':
            date = parse(date_time_param)
            strdate = date.strftime('%y%m%d')
        else:
            strdate = datetime.today().strftime('%y%m%d')

        ssm = boto3.client('ssm')

        filename = instance_id+'_'+strdate+'.log'

        parameters2 = {'commands': [
            'copy u_ex'+strdate+'.log iislog.log',
            'aws s3 cp iislog.log s3://movidesk-log/temp/'+filename],
            'executionTimeout': ['3600'],
            'workingDirectory': ['C:\\inetpub\\logs\\LogFiles\\W3SVC1\\']
        }

        ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunPowerShellScript',
            TimeoutSeconds=600,
            Parameters=parameters2)

        return_json = {'fulfillmentText': 'Comando enviado. Arquivo: ' + filename}
        return return_json
