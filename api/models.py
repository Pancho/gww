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


class TestBundle(models.Model):
	created = models.DateTimeField()
	ends = models.DateTimeField()



class TestPage(models.Model):
	name = models.TextField()
	slug = models.TextField()
	template_path = models.TextField()
	bundle = models.ForeignKey(to=TestBundle, blank=False, null=False)


	def __unicode__(self):
		return '%s, available on "%s" with template %s; %d tests performed so far' % (self.name, self.slug, self.template_path, self.datadump_set.filter(parent=None).count())


class DataDump(models.Model):
	test_uuid = models.CharField(max_length=36)
	timestamp = models.DateTimeField(auto_now_add=True)
	type = models.IntegerField(choices=DATA_DUMP_TYPES)
	data = JSONField(default='{}')
	custom = JSONField(default='{}')
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