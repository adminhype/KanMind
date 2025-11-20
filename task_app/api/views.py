from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from task_app.models import Task, Comment
from .permissions import TaskPermission
from .serializers import TaskCreateSerializer, TaskReadSerializer, TaskUpdateSerializer, CommentSerializer


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


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskReadSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = TaskReadSerializer(instance)

        return Response(response_serializer.data)


class TaskCommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        if self.request.user not in task.board.members.all():
            raise PermissionDenied(
                "you must be a board member to view comments")
        return task.comments.all().order_by('created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        if self.request.user not in task.board.members.all():
            raise PermissionDenied(
                "you must be a board member to add comments")
        serializer.save(author=self.request.user, task=task)
