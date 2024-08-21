from django.urls import path
from . import views as task_view


urlpatterns = [
    path('tasks/', task_view.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', task_view.TaskDetailView.as_view(), name='task-detail'),

    path('tasks/<int:task_id>/comments/', task_view.CommentListCreateView.as_view(), name='comment-list-create'),
    path('tasks/<int:task_id>/comments/<int:pk>/', task_view.CommentDetailView.as_view(), name='comment-detail'),

]
