import json
from api.models import TestPage


DATA_DUMP_EXAMPLE = '{"header": {"bundle": 1,"page": 1,"baseTime": 1337501361954,"timeStamp": 1337501347182},"data": [{"data": {},"totalHeapSize": 10198272,"type": -1,"usedHeapSize": 5012132,"time": 131.0302734375,"sequence": 0},{"children": [{"children": [],"data": {"scriptLine": 106,"scriptName": "chrome-extension://onnlpicjkjbhcimimoipdhmbgnfdcmhb/headless_content_script.js"},"totalHeapSize": 11181056,"type": 15,"usedHeapSize": 5687712,"duration": 3,"time": 1439.030029296875}],"data": {"type": "DOMContentLoaded"},"totalHeapSize": 11181056,"type": 0,"usedHeapSize": 5687712,"duration": 3,"time": 1439.030029296875,"sequence": 25}]}'

from django.test import TestCase


class QueueTest(TestCase):
	def test_consumer(self):
		test_page = TestPage.objects.get(id=1)
		data = json.loads(DATA_DUMP_EXAMPLE)


