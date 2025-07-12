from django.contrib import admin
from .models import Accommodation, Student, Application,AccommodationImage

# Register your models here.
admin.site.register(Accommodation)
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(AccommodationImage)
