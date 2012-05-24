from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
	url(r'^$', 'index', name = 'api.index'),
	url(r'^/tests$', 'tests', name = 'api.tests'),
)
