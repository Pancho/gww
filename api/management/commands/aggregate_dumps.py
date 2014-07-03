import logging

from django.core.management.base import NoArgsCommand

import api


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

	def handle_noargs(self, **options):
		api.aggregate_dumps()