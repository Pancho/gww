import json
import random
import uuid


from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from api import models
from greenww import settings


PAGE_CACHE = {}


def index(request):
	active_bundles = models.TestBundle.objects.all()
	# Due to the experienced problems with logging, I'm reverting to only one active window at a time and then changing the url to achieve same result with linear progression
	# This is production ready, but not even closely prepared for multiple bundle testing
	# Proposal: randomly select one bundle for one user for one click
	bundle = random.choice(active_bundles)
	page = bundle.testpage_set.all().order_by('id')[0]  # Take first
	ctx = {
		'selected': 'index',
		'first_test_page_slug': page.slug,
	}
	return render_to_response('pages/index.html', ctx, RequestContext(request))


def test(request, slug):
	if slug not in PAGE_CACHE:
		page = models.TestPage.objects.get(slug=slug)
		PAGE_CACHE.update({
			slug: {
				'template_path': page.template_path,
				'next_slug': page.next_page.slug,
			}
		})

	ctx = {
		'site': settings.CURRENT_SITE_DOMAIN,
		'next': PAGE_CACHE.get(slug).get('next_slug'),
		'test_page': True, 'test_uuid': str(uuid.uuid4()),
		'ip': request.META.get('REMOTE_ADDR', None),
	}
	return render_to_response(PAGE_CACHE.get(slug).get('template_path'), ctx, RequestContext(request))


def view_tests(request, bundle_id=None):
	selected_bundle = None
	if bundle_id:
		selected_bundle = models.TestBundle.objects.get(id=bundle_id)
	ctx = {
		'site': settings.CURRENT_SITE_DOMAIN,
		'selected': 'tests',
		'bundles': models.TestBundle.objects.all(),
		'selected_bundle': selected_bundle,
	}
	return render_to_response('pages/tests.html', ctx, RequestContext(request))


def view_test(request, slug):
	test_page = models.TestPage.objects.get(slug=slug)
	ctx = {
		'test_page': False,
	}
	return render_to_response(test_page.template_path, ctx, RequestContext(request))


def results(request):
	ctx = {
		'selected': 'results',
		'bundles': models.TestBundle.objects.all(),
	}
	return render_to_response('pages/results.html', ctx, RequestContext(request))


def results_bundle(request, bundle_id):
	selected_bundle = None
	if bundle_id:
		selected_bundle = models.TestBundle.objects.get(id=bundle_id)
	ctx = {
		'selected': 'results',
		'bundles': models.TestBundle.objects.all(),
		'selected_bundle': selected_bundle,
	}
	return render_to_response('pages/results_bundle.html', ctx, RequestContext(request))


def results_test(request, test_slug=None):
	selected_test = None
	selected_bundle = None
	if test_slug:
		selected_test = models.TestPage.objects.get(slug=test_slug)
		selected_bundle = selected_test.bundle
	if selected_test is None:
		raise Http404
	ctx = {
		'selected': 'results',
		'bundles': models.TestBundle.objects.all(),
		'selected_bundle': selected_bundle,
		'selected_test': selected_test,
	}
	return render_to_response('pages/results_test.html', ctx, RequestContext(request))


def article(request, article_slug=None):
	return_type = request.GET.get('type', False)
	if article_slug is not None:
		selected_article = models.Article.objects.get(slug=article_slug)
	else:
		selected_article = models.Article.objects.all()[0]
	if return_type == 'json':
		return HttpResponse(json.dumps(model_to_dict(selected_article)))
	elif return_type == 'html':
		ctx = {
			'selected_article': selected_article,
		}
		return render_to_response('blocks/article.html', ctx, RequestContext(request))
	else:
		ctx = {
			'selected_article': selected_article,
			'articles': models.Article.objects.order_by('title'),
		}
		return render_to_response('pages/article.html', ctx, RequestContext(request))
