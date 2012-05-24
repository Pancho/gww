from django.conf.urls import patterns, url


urlpatterns = patterns('www.views',
	url(r'^$', 'index', name='www.index'),

	# Test pages
	url(r'^test/(?P<slug>[\-\w]+)$', 'test', name='www.test'),
	url(r'^test/display/(?P<slug>[\-\w]+)$', 'test_display', name='www.test_display'),
	url(r'^speed-tracer-not-found$', 'speed_tracer_not_found', name='www.speed_tracer_not_found'),

    #Test test page :)
	url(r'^example$', 'example', name='www.example'),
)
  