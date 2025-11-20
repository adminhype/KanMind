from rest_framework import serializers


from django.contrib.auth.models import User


from task_app.models import Task, Comment
from board_app.models import Board


class TaskCreateSerializer(serializers.ModelSerializer):
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

        if user not in board.members.all():
            raise serializers.ValidationError(
                {"permission": "You must be a board member to create tasks."}
            )

        assignee = data.get('assignee')
        if assignee and assignee not in board.members.all():
            raise serializers.ValidationError(
                {"assignee_id": "Assignee must be board member."}
            )

        reviewer = data.get('reviewer')
        if reviewer and reviewer not in board.members.all():
            raise serializers.ValidationError(
                {"reviewer_id": "Reviewer must be board member."}
            )
        return data

    def create(self, validated_data):
        creator = self.context['request'].user

        task = Task.objects.create(creator=creator, **validated_data)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
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
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']

    def get_fullname(self, obj):
        full = obj.get_full_name()
        return full if full else obj.username


class CommentSerializer(serializers.ModelSerializer):
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
