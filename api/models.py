from django.db import models
from api.modelfields import JSONField


DATA_DUMP_TYPES = (
	(-1, 'UNKNOWN'),
	(0, 'DOM_EVENT'),
	(1, 'LAYOUT'),
	(2, 'RECALC_STYLE'),
	(3, 'PAINT'),
	(4, 'PARSE_HTML'),
	(5, 'TIMER_INSTALLED'),
	(6, 'TIMER_CLEARED'),
	(7, 'TIMER_FIRED'),
	(8, 'XHR_READY_STATE_CHANGE'),
	(9, 'XHR_LOAD'),
	(10, 'EVAL_SCRIPT'),
	(11, 'LOG_MESSAGE'),
	(12, 'NETWORK_RESOURCE_START'),
	(13, 'NETWORK_RESOURCE_RESPONSE'),
	(14, 'NETWORK_RESOURCE_FINISH'),
	(15, 'JAVASCRIPT_CALLBACK'),
	(16, 'RESOURCE_DATA_RECEIVED'),
	(17, 'GC_EVENT'),
	(18, 'MARK_DOM_CONETNT'),
	(19, 'MARK_LOAD_EVENT'),
)
DATA_DUMP_TYPES_HUMANIZE = (
	(-1, 'Unknown'),
	(0, 'DOM Event'),
	(1, 'Layout'),
	(2, 'Recalc Style'),
	(3, 'Paint'),
	(4, 'Parse HTML'),
	(5, 'Timer Installed'),
	(6, 'Timer Cleared'),
	(7, 'Timer Fired'),
	(8, 'XHR Ready State Change'),
	(9, 'XHR Load'),
	(10, 'Eval Script'),
	(11, 'Log Message'),
	(12, 'Network Resource Start'),
	(13, 'Network Resource Response'),
	(14, 'Network Resource Finish'),
	(15, 'JavaScript Callback'),
	(16, 'Resource Data Reveiced'),
	(17, 'Garbage Collector Event'),
	(18, 'Mark Dom Content'),
	(19, 'Mark Load Event'),
)


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
	type = models.IntegerField(choices=DATA_DUMP_TYPES, db_index=True)
	data = JSONField(default='{}')
	custom = JSONField(default='{}')
	user_agent = models.TextField()
	ip = models.TextField()
	was_hidden = models.NullBooleanField()
	platform = models.TextField()
	source = models.TextField(db_index=True) # The id generated on the client and stored in localStorage there. This is the bare minimum I can do to ensure I have any data on the uniqueness of the datadump's source
	duration = models.FloatField(null=True, blank=True) # Not always <> 0, some events don't return duration.
	parent = models.ForeignKey('self', null=True, blank=True)
	test_page = models.ForeignKey(to=TestPage, null=True, blank=True) # If it's a child, then this is null, as it's connected to the test page through it's top parent


	def get_test_page(self):
		return self.test_page


	def get_immediate_children(self):
		#return immediate children of this dump
		return self.datadump_set.all()


	def resolve_type(self):
		return dict(DATA_DUMP_TYPES).get(self.type, self.type)


	def __unicode__(self):
		return '%s for %s' % (self.get_test_page().name, self.resolve_type())


class BundleResult(models.Model):
	browser_id = models.TextField()
	title = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	bundle = models.ForeignKey(to=TestBundle)


class ResultColumn(models.Model):
	value = models.FloatField()
	secondary_values = JSONField(default='{}')
	type = models.IntegerField(choices=DATA_DUMP_TYPES, db_index=True)
	test = models.ForeignKey(to=TestPage)
	bundle_result = models.ForeignKey(to=BundleResult)


class Article(models.Model):
	title = models.TextField()
	slug = models.TextField()
	abstract = models.TextField(null=True, blank=True)
	content = models.TextField()