from django.urls import path


from .views import TasksAssignedToMeView


urlpatterns = [
    path("tasks/assigned-to-me/", TasksAssignedToMeView.as_view(),
         name="tasks-assigned-to-me"),
]
