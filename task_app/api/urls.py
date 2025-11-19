from django.urls import path


from .views import TaskCreateView, TasksAssignedToMeView, TasksReviewingView


urlpatterns = [
    path("tasks/assigned-to-me/", TasksAssignedToMeView.as_view(),
         name="tasks-assigned-to-me"),
    path("tasks/reviewing/", TasksReviewingView.as_view(),
         name="tasks-reviewing"),
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
]
