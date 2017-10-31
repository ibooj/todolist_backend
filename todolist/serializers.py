import json

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from .models import Task, SubTask


class CustomViewRelatedField(serializers.ModelField):
    default_error_messages = {
        'invalid': _('Value must be valid JSON.')
    }

    def __init__(self, model_field, view_fields=None, **kwargs):
        self.view_fields = view_fields
        super(CustomViewRelatedField, self).__init__(model_field, allow_null=True, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            value = data.get('id')
        else:
            try:
                json_data = json.loads(data)
                value = json_data.get('id')
            except (TypeError, ValueError):
                self.fail('invalid')
        try:
            return self.model_field.related_model.objects.get(pk=value)
        except (TypeError, ValueError, ObjectDoesNotExist):
            pass

    def to_representation(self, obj):
        o = getattr(obj, self.model_field.name)
        if o:
            d = {'id': o.id}
            for f in self.view_fields:
                attr = getattr(o, f)
                if callable(attr):
                    attr = attr()
                    f = str(f).replace('get_', '')
                d.update({f: attr})
            return d


class SubTaskSerializer(serializers.ModelSerializer):
    task = CustomViewRelatedField(model_field=SubTask()._meta.get_field('task'), view_fields=['id'])

    class Meta:
        model = SubTask
        fields = ('id', 'name', 'date_create', 'status', 'task')

    def validate_task(self, task):
        if task.owner != self.context['request'].user:
            raise PermissionDenied
        return task


class TaskSerializer(serializers.ModelSerializer):
    sub_tasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'date_create', 'sub_tasks')
