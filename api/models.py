from django.db import models


from api.modelfields import JSONField


class TestBundle(models.Model):
	created = models.DateTimeField()
	title = models.TextField()
	description = models.TextField()
	ends = models.DateTimeField()
	aggregate_dumps = models.TextField()


	def get_ordered_test_pages(self):
		return self.testpage_set.order_by('order')


	def get_aggregate_dumps_as_list(self):
		return [int(x) for x in self.aggregate_dumps.split(',')]



class TestPage(models.Model):
	name = models.TextField()
	slug = models.TextField()
	description = models.TextField()
	screenshot = models.TextField()
	screenshot_width = models.IntegerField()
	screenshot_height = models.IntegerField()
	template_path = models.TextField()
	order = models.IntegerField()
	bundle = models.ForeignKey(to=TestBundle, blank=False, null=False)
	next_page = models.ForeignKey('self', null=True, blank=True)


	def __unicode__(self):
		return '%s, available on "%s" with template %s; %d tests performed so far' % (self.name, self.slug, self.template_path, self.datadump_set.filter(parent=None).count())


class DataDump(models.Model):
	test_uuid = models.CharField(max_length=36, db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	data = JSONField(default='{}')
	custom = JSONField(default='{}')
	user_agent = models.TextField()
	ip = models.TextField()
	was_hidden = models.NullBooleanField()
	platform = models.TextField()
	source = models.TextField(db_index=True)  # The id generated on the client and stored in localStorage there. This is the bare minimum I can do to ensure I have any data on the uniqueness of the datadump's source
	duration = models.FloatField(null=True, blank=True)
	test_page = models.IntegerField()  # Just save the TestPage id - good enough


	def get_test_page(self):
		return TestPage.objects.get(id=self.test_page)


	def __unicode__(self):
		return '%s (%s)' % (self.get_test_page().name, self.duration)


class BundleResult(models.Model):
	browser_id = models.TextField()
	title = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	bundle = models.ForeignKey(to=TestBundle)


class ResultColumn(models.Model):
	value = models.FloatField()
	secondary_values = JSONField(default='{}')
	test = models.ForeignKey(to=TestPage)
	bundle_result = models.ForeignKey(to=BundleResult)


class Article(models.Model):
	title = models.TextField()
	slug = models.TextField()
	abstract = models.TextField(null=True, blank=True)
	content = models.TextField()