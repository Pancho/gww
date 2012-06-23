import json
from math import sqrt

from api import models


def aggregate_dumps():
	browser_ids = models.DataDump.objects.values_list('source', flat=True).distinct() # Get all the different users

	for browser_id in browser_ids:
		for bundle in models.TestBundle.objects.all():
			bundle_result = models.BundleResult()
			bundle_result.browser_id = browser_id
			bundle_result.title = 'Results for "%s"' % bundle.title
			bundle_result.bundle =  bundle
			bundle_result.save()

			for dump_type in bundle.get_aggregate_dumps_as_list():
				for test_page in bundle.testpage_set.all():

					mean, std_dev = mean_standard_dev([x for x in models.DataDump.objects.filter(source=browser_id).filter(type=dump_type).filter(test_page=test_page).values_list('duration', flat=True) if x > 0])

					result_column = models.ResultColumn()
					result_column.bundle_result = bundle_result
					result_column.test = test_page
					result_column.type = dump_type
					result_column.value = mean
					result_column.secondary_values = json.dumps({'std_dev': std_dev})
					result_column.save()


def print_results():
	for bundle_result in models.BundleResult.objects.all():
		print bundle_result.title

		for column in bundle_result.resultcolumn_set.order_by('test__id'):
			print "%s (%s): %f" % (column.test.name, dict(models.DATA_DUMP_TYPES_HUMANIZE).get(column.type, -1), column.value)

		print ''


def clean_results():
	models.BundleResult.objects.all().delete()
	models.ResultColumn.objects.all().delete()



def mean_standard_dev(x):
	n, mean, std = len(x), 0, 0
	for a in x:
		mean += a
	mean /= float(n)
	for a in x:
		std += (a - mean) ** 2
	std = sqrt(std / float(n-1))
	return mean, std