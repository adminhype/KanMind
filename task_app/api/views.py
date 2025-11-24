from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from board_app.models import Board
from task_app.models import Task, Comment
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor
from .serializers import TaskCreateSerializer, TaskReadSerializer, TaskUpdateSerializer, CommentSerializer, TaskUpdateResponseSerializer


class TaskCreateView(CreateAPIView):
    """
    endpoint to create a new task 
    POST /api/tasks/
    """
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # fix 400 too 404, if board not found
        board_id = request.data.get('board')
        if board_id:
            get_object_or_404(Board, id=board_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        # return full task data
        response_serializer = TaskReadSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TasksAssignedToMeView(ListAPIView):
    """
    endpoint to get tasjs assigned to current user
    GET /api/tasks/assigned-to-me/
    """
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
    """
    endpoint to get tasks reviewed by current user
    GET /api/tasks/reviewing/
    """
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
    """
    endpoint to retrieve, update or delete a task
    GET/PATCH/DELETE /api/tasks/{id}/
    """
    queryset = Task.objects.all()

    def get_permissions(self):
        """
        dynamic permissions based on action.
        DELETE: Creator or Board Owner only.
        UPDATE/GET: Board Member only.
        """
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]

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

        # return full task structure
        response_serializer = TaskUpdateResponseSerializer(instance)
        return Response(response_serializer.data)


class TaskCommentView(ListCreateAPIView):
    """
    endpoint to list and create comments for a task.
    GET/POST /api/tasks/{id}/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        # check board membership(403 forbidden)
        if self.request.user != task.board.owner and self.request.user not in task.board.members.all():
            raise PermissionDenied(
                "you must be a board member to view comments")
        return task.comments.all().order_by('created_at')

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        if self.request.user != task.board.owner and self.request.user not in task.board.members.all():
            raise PermissionDenied(
                "you must be a board member to add comments")
        serializer.save(author=self.request.user, task=task)


class TaskCommentDeleteView(DestroyAPIView):
    """
    endpoint to delete a comment.
    DELETE /api/tasks/{id}/comments/{comment_id}/
    """
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('pk')

        comment = get_object_or_404(Comment, id=comment_id, task__id=task_id)
        self.check_object_permissions(self.request, comment)
        return comment
