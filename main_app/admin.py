from django.contrib import admin

from main_app.models import Appointments

# Register your models here.

admin.site.register(Appointments)

admin.site.site_header = 'NovaCare Administration'

admin.site.site_title = 'NovaCare Administration'

# novacare@gmail.com
# nova