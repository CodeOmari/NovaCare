from django.contrib import admin

from main_app.models import Appointment, Patient

# Register your models here.

admin.site.register(Appointment)
admin.site.register(Patient)

admin.site.site_header = 'NovaCare Administration'

admin.site.site_title = 'NovaCare Administration'

# novacare@gmail.com
# novacare