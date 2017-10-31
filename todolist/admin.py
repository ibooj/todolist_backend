from django.contrib import admin

from .models import Task, SubTask


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'date_create')
    raw_id_fields = ('owner',)


@admin.register(SubTask)
class SubTask(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'task', 'date_create')
    raw_id_fields = ('owner', 'task')
