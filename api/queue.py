import json
import pika
import pprint
from api.models import DataDump, TestPage


def post_to_provider(json):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='json_data_dump')
	channel.basic_publish(exchange='', routing_key='json_data_dump', body=json)
	connection.close()


def consume_from_queue():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='json_data_dump')
	channel.basic_consume(data_dump_callback, queue='json_data_dump', no_ack=False)

	channel.start_consuming()


def data_dump_callback(channel, method, properties, body):
	try:
		body_dict = json.loads(body)
	except Exception, e:
		channel.basic_ack(method.delivery_tag) # Acknowledge message, since the body isn't a JSON... we should just forget it

	try:
		data = body_dict.get('data', [])
		header = body_dict.get('header', {})
		test_page = TestPage.objects.get(id=header.get('page', -1))

		save_data_dump(data, header, None, test_page)

		channel.basic_ack(method.delivery_tag) # Acknowledge message, delete from queue (pack this into "transaction")
	except Exception, e:
		print e

def save_data_dump(children, header, parent, test_page):
		for data in children:
			data_dump = DataDump()
			data_dump.user_agent = header.get('userAgent', 'unknown')
			data_dump.platform = header.get('platform', 'unknown')
			data_dump.test_uuid = header.get('test_uuid', 'useless')
			data_dump.type = data.get('type', -1)
			data_dump.data = json.dumps(data.get('data', {}))
			data_dump.custom = json.dumps(header)
			data_dump.duration = data.get('duration', 0)
			data_dump.test_page = test_page
			if parent is not None:
				data_dump.parent = parent
			data_dump.save()

			if len(data.get('children', [])):
				save_data_dump(data.get('children', []), header, data_dump, test_page)
