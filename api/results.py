import json


from api import models


def save_result_dump(request, blob):
	start = int(blob.get('start'))
	end = int(blob.get('end'))

	data_dump = models.DataDump()

	data_dump.user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
	data_dump.platform = blob.get('platform', 'unknown')
	data_dump.test_uuid = blob.get('test_uuid', 'unknown')
	data_dump.source = blob.get('source', 'unknown')
	data_dump.ip = request.META.get('REMOTE_ADDR', 'unknown')
	data_dump.was_hidden = blob.get('was_hidden', None)
	data_dump.data = json.dumps(blob.get('performance', {}))
	data_dump.duration = end - start
	data_dump.test_page = int(blob.get('page'))

	data_dump.save()