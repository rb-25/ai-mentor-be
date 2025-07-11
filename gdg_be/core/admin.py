from django.contrib import admin
from gdg_be.core.models import Resource, Project, Step, UserProject

# Register your models here.
admin.site.register(Resource)
admin.site.register(Project)
admin.site.register(Step)
admin.site.register(UserProject)
