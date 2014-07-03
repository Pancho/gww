from django.conf.urls import patterns, url


urlpatterns = patterns('www.views',
	url(r'^$', 'index', name='www.index'),

	# Test pages
	url(r'^test/(?P<slug>[\-\w]+)$', 'test', name='www.test'),
    # Test pages
	url(r'^view-tests$', 'view_tests', name='www.view_tests'),
	url(r'^view-tests/bundle/(?P<bundle_id>\d+)$', 'view_tests', name='www.view_bundle'),
	url(r'^view-tests/display/(?P<slug>[\-\w]+)$', 'view_test', name='www.view_test'),
    # Results/stats pages
    url(r'^results$', 'results', name='www.results'),
    url(r'^results/bundle/(?P<bundle_id>\d+)$', 'results_bundle', name='www.results_bundle'),
    url(r'^results/test/(?P<test_slug>[\-\w]+)$', 'results_test', name='www.results_test'),
    # Article
    url(r'^article/$', 'article', name='www.article'),
    url(r'^article/(?P<article_slug>[\-\w]+)$', 'article', name='www.article'),
)
