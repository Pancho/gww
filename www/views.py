import uuid
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from api.models import TestPage
from greenww import settings


PAGE_CACHE = {}


def index(request):
	ctx = {}
	return render_to_response('pages/index.html', ctx, RequestContext(request))


def test(request, slug):
	if slug not in PAGE_CACHE:
		page = TestPage.objects.get(slug=slug)
		PAGE_CACHE.update({
			slug: page.template_path
		})

	ctx = {
		'site': settings.CURRENT_SITE_DOMAIN,
		'test_page': True,
		'test_uuid': str(uuid.uuid4())
	}
	return render_to_response(PAGE_CACHE.get(slug), ctx, RequestContext(request))


def test_display(request, slug):
	test_page = TestPage.objects.get(slug=slug)
	ctx = {
		'test_page': False
	}
	return render_to_response(test_page.template_path, ctx, RequestContext(request))


def speed_tracer_not_found(request):
	ctx = {}
	return render_to_response('pages/speedtracer_not_detected.html', ctx, RequestContext(request))


def example(request):
	ctx = {}
	return render_to_response('tests/solucija-1/index.html', ctx, RequestContext(request))
