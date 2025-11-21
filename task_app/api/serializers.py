from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth.models import User


from task_app.models import Task, Comment
from board_app.models import Board


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    serializer for creating a task.
    accept Ids for relations.
    """
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, source='assignee')
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, source='reviewer')

    class Meta:
        model = Task
        fields = [
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]

    def validate(self, data):
        user = self.context['request'].user
        board = data['board']

        # API DOC requires 403 Forbiddenif not member
        if user != board.owner and user not in board.members.all():
            raise PermissionDenied(
                "you must be a board member to create tasks.")
        self._validated_members(board, data.get('assignee'), "assignee_id")
        self._validated_members(board, data.get('reviewer'), "reviewer_id")
        return data

    def _validated_members(self, board, user, field_name):
        if user and user != board.owner and user not in board.members.all():
            raise serializers.ValidationError(
                {field_name: "Must be a board member."}
            )

    def create(self, validated_data):
        creator = self.context['request'].user
        return Task.objects.create(creator=creator, **validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    serializer for updating a task.
    """
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, source='assignee')
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, source='reviewer')

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date',
        ]

    def validate(self, data):
        task = self.instance
        board = task.board

        if 'assignee' in data:
            assignee = data['assignee']
            if assignee and assignee not in board.members.all():
                raise serializers.ValidationError(
                    {"assignee_id": "Assignee must be board member."}
                )

        if 'reviewer' in data:
            reviewer = data['reviewer']
            if reviewer and reviewer not in board.members.all():
                raise serializers.ValidationError(
                    {"reviewer_id": "Reviewer must be board member."}
                )
        return data


class UserPreviewSerializer(serializers.ModelSerializer):
    """
    serializer for displaying user info in task.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']

    def get_fullname(self, obj):
        full = obj.get_full_name()
        return full if full else obj.username


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for comments.
    """
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'created_at',
            'author',
            'content'
        ]

    def get_author(self, obj):
        full = obj.author.get_full_name()
        return full if full else obj.author.username


class TaskReadSerializer(serializers.ModelSerializer):
    """
    serializer for reading task data (nested objects).
    """
    assignee = UserPreviewSerializer(read_only=True)
    reviewer = UserPreviewSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskUpdateResponseSerializer(serializers.ModelSerializer):
    """
    serializer specific for PATCH response.
    exlucdes "board and "comments_count" to match API DOC.
    """
    assignee = UserPreviewSerializer(read_only=True)
    reviewer = UserPreviewSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
        ]
