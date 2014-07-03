from django.contrib import admin


import api


admin.site.register(api.models.TestPage)
admin.site.register(api.models.TestBundle)
admin.site.register(api.models.DataDump)
