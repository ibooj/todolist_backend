from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class OwnerObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerObjectPermission]


class SubTaskCreateAPIView(generics.CreateAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status=False)


class SubTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, OwnerObjectPermission]
    http_method_names = ['post', 'patch', 'delete', 'options']

    def perform_update(self, serializer):
        serializer.save(task=self.get_object().task)
