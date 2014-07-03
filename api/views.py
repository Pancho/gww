# FORMATTING JSON FLOATS
import json
import random
from json import encoder


from django.http import HttpResponse


from api import models
from api import results
from greenww import settings


encoder.FLOAT_REPR = lambda o: format(o, '.2f')
GIF = 'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'


def index(request):
	blob = json.loads(request.GET.get('blob'))
	try:
		results.save_result_dump(request, blob)
	except Exception, e:
		pass # We really don't care if we miss one
	return HttpResponse(GIF, mimetype='image/gif') # return the image


def tests(request):
	active_bundles = models.TestBundle.objects.all()

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

	columns = ['Test', 'DOM Processing Time']

	for test in bundle_result.bundle.testpage_set.all():
		chart = [test.name]
		chart.extend([x for x in bundle_result.resultcolumn_set.filter(test=test).values_list('value', flat=True)])
		charts.append(chart)

	result = {
		'title': bundle_result.title,
		'columns': columns,
		'charts': charts,
	}

	return HttpResponse(json.dumps(result), mimetype='application/json')