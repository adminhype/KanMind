from django.urls import path


from .views import TaskCommentDeleteView, TaskCreateView, TaskDetailView, TasksAssignedToMeView, TasksReviewingView, TaskCommentView


urlpatterns = [
    path("tasks/assigned-to-me/", TasksAssignedToMeView.as_view(),
         name="tasks-assigned-to-me"),
    path("tasks/reviewing/", TasksReviewingView.as_view(),
         name="tasks-reviewing"),
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:task_id>/comments/",
         TaskCommentView.as_view(), name="task-comments"),
    path("tasks/<int:task_id>/comments/<int:pk>/",
         TaskCommentDeleteView.as_view(), name="task-comment-delete"),
]
