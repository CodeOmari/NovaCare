from django.contrib import admin

from main_app.models import AdultPatient, ChildPatient

# Register your models here.

admin.site.register(AdultPatient)

admin.site.register(ChildPatient)

admin.site.site_header = 'NovaCare Administration'

admin.site.site_title = 'NovaCare Administration'

#NCadmin@gmail.com