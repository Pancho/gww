from django.contrib import admin
import api


admin.site.register(api.models.TestPage)
admin.site.register(api.models.TestBundle)

class DataDumpAdmin(admin.ModelAdmin):
	readonly_fields = ('parent',) # This can kill everything...
	search_fields = ['=test_uuid', '=type']

admin.site.register(api.models.DataDump, DataDumpAdmin)
