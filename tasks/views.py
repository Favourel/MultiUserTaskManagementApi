from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from users.views import notify_user
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ['due_date', 'status']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Task.objects.all()
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)
        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_update(self, serializer):
        task = serializer.instance
        if task.assigned_to == self.request.user or self.request.user.is_admin:
            serializer.save()

        if serializer.instance.assigned_to != self.request.user:
            notify_user(serializer.instance.assigned_to,
                        f"The task '{serializer.instance.title}' has been updated.")

        else:
            raise PermissionDenied("You do not have permission to update this task.")


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return Comment.objects.filter(task=task)

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer.save(created_by=self.request.user, task=task)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return Comment.objects.filter(task=task)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.created_by or self.request.user.is_admin:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this comment.")
