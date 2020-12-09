from django.contrib import admin
from accountapp.models import User, Company, Department, Position

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Position)
