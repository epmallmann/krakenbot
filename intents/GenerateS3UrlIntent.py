from intents.Intent import Intent
import boto3


class GenerateS3UrlIntent(Intent):

    def run(self):
        s3_log_file = self.event['queryResult']['parameters']['S3LogFile']

        s3 = boto3.client('s3')

        params = {
            'Bucket': 'movidesk-log',
            'Key': 'temp/' + s3_log_file
        }

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params=params
        )

        return_json = {'fulfillmentText': url}
        return return_json

