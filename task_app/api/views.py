from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from task_app.models import Task
from .serializers import TaskCreateSerializer, TaskReadSerializer


class TaskCreateView(CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        response_serializer = TaskReadSerializer(task)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TasksAssignedToMeView(ListAPIView):
    serializer_class = TaskReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).select_related(
            'assignee',
            'reviewer',
            'board'
        )


class TasksReviewingView(ListAPIView):
    serializer_class = TaskReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user).select_related(
            'assignee',
            'reviewer',
            'board'
        )
