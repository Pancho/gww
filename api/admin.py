from django.contrib import admin
import api


admin.site.register(api.models.TestPage)

class DataDumpAdmin(admin.ModelAdmin):
	readonly_fields = ('parent',) # This can kill everything...

admin.site.register(api.models.DataDump, DataDumpAdmin)
