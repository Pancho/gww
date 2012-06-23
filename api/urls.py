from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
	url(r'^$', 'index', name = 'api.index'),
	url(r'^/tests$', 'tests', name = 'api.tests'),
	url(r'^/results/bundle/(?P<bundle_id>\d+)/(?P<browser_id>[\-\w]+)/$', 'results_bundle', name='api.results_bundle'),
)
