from django.contrib import admin
from todo.models import TodosModel, GroupModel

# Register your models here.
admin.site.register(TodosModel)
admin.site.register(GroupModel)
