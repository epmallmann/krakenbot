from intents.Intent import Intent
from botocore.vendored import requests
import json


class TicketCreateIntent(Intent):

	def run(self):
		return_json = {}
		person = {'id': '539639646'}
		md_url = 'https://api.movidesk.com/public/v1/tickets?token=458271a5-ff51-4753-ad2a-e7f366adee6b'
		
		subject = self.event['queryResult']['parameters']['subject']
		
		data_post = {
			'type': 1,
			'createdBy': person,
			'subject': subject,
			'category': 'Solicitação de serviço',
			'urgency': 'Alta',
			'status': 'Novo',
			'clients': [person],
			'actions': [{'id': 1,'type': 1, 'description': subject}]
		}

		r = requests.post(md_url, json=data_post)
		print(r.status_code, r.reason)
		print(r.text)
		
		post_return_json = json.loads(r.text)
		msg = 'Ticket aberto: https://testes.movidesk.com/Ticket/Edit/' + str(post_return_json['id'])
		
		return_json = {'fulfillmentText': msg}
		return return_json

