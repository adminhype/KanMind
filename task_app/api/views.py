from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from task_app.models import Task
from .serializers import AssignedToMeSerializer


class TasksAssignedToMeView(ListAPIView):
    serializer_class = AssignedToMeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).select_related(
            'assignee',
            'reviewer',
            'board'
        )
