from django.urls import path


from .views import TaskCreateView, TaskDetailView, TasksAssignedToMeView, TasksReviewingView


urlpatterns = [
    path("tasks/assigned-to-me/", TasksAssignedToMeView.as_view(),
         name="tasks-assigned-to-me"),
    path("tasks/reviewing/", TasksReviewingView.as_view(),
         name="tasks-reviewing"),
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
