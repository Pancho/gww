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
			bundle_result.bundle = bundle

			bundle_result.save()

			for test_page in bundle.testpage_set.all():
				durations = models.DataDump.objects.filter(source=browser_id).filter(test_page=test_page.id).values_list('duration', flat=True)
				if len(durations) > 0:
					mean, std_dev = mean_standard_dev(durations)

					result_column = models.ResultColumn()

					result_column.bundle_result = bundle_result
					result_column.test = test_page
					result_column.value = mean
					result_column.secondary_values = json.dumps({'std_dev': std_dev})

					result_column.save()


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
	std = sqrt(std / float(n - 1))
	return mean, std