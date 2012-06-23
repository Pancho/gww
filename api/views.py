from datetime import datetime
import decimal
import json
import random
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api import queue, models


# FORMATTING JSON FLOATS
from json import encoder
from greenww import settings


encoder.FLOAT_REPR = lambda o: format(o, '.2f')

@csrf_exempt
def index(request):
	# Just save into the provider
	queue.post_to_provider(request.raw_post_data)

	return HttpResponse(json.dumps({'status': 'ok'}))


def tests(request):
	now_timestamp = datetime.now()
	active_bundles = models.TestBundle.objects.filter(created__lt=now_timestamp).filter(ends__gt=now_timestamp)

	result = {
		'meta': {
			'domain': settings.CURRENT_SITE_DOMAIN
		},
		'pages': []
	}

	# Due to the experienced problems with logging, I'm reverting to only one active window at a time and then changing the url to achieve same result with linear progression
	# This is production ready, but not even closely prepared for multiple bundle testing
	# Proposal: randomly select one bundle for one user for one click
	bundle = random.choice(active_bundles)
	page = bundle.testpage_set.all().order_by('id')[0] # Take first
	result['pages'].append({'page': page.id, 'slug': page.slug, })

	return HttpResponse(json.dumps(result), mimetype='application/json')



def results_bundle(request, bundle_id, browser_id):
	bundle_result = models.BundleResult.objects.filter(bundle_id=bundle_id, browser_id=browser_id).order_by('-timestamp')[0]

	charts = []

	bundle_result_column_types = bundle_result.bundle.get_aggregate_dumps_as_list()
	bundle_result_column_types.sort()

	columns = ['Test']
	columns.extend([dict(models.DATA_DUMP_TYPES_HUMANIZE).get(x) for x in bundle_result_column_types])

	for test in bundle_result.bundle.testpage_set.all():
		chart = [test.name]
		chart.extend([x for x in bundle_result.resultcolumn_set.filter(test=test).order_by('type').values_list('value', flat=True)])
		charts.append(chart)

	result = {
		'title': bundle_result.title,
		'columns': columns,
		'charts': charts,
#		'timestamp': bundle_result.timestamp,
	}

	return HttpResponse(json.dumps(result), mimetype='application/json')