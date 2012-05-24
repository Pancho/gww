from datetime import datetime
import json
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api import queue
from api.models import TestBundle


@csrf_exempt
def index(request):
	# Just save into the provider
	queue.post_to_provider(request.raw_post_data)

	print dir(request)
	print request.META

	return HttpResponse(json.dumps({'status': 'ok'}))


def tests(request):
	now_timestamp = datetime.now()
	active_bundles = TestBundle.objects.filter(created__lt=now_timestamp).filter(ends__gt=now_timestamp)

	site = Site.objects.get_current()

	result = {
		'meta': {
			'domain': site.domain
		},
		'pages': []
	}

	for bundle in active_bundles:
		for page in bundle.testpage_set.all():
			result['pages'].append({'page': page.id, 'slug': page.slug, })

	return HttpResponse(json.dumps(result), mimetype='application/json')