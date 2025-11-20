from rest_framework import serializers

from django.contrib.auth.models import User

from board_app.models import Board
from task_app.models import Task


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField(read_only=True)
    ticket_count = serializers.SerializerMethodField(read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField(read_only=True)

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'members',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


class BoardMemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'fullname',
        ]

    def get_fullname(self, obj):
        full = obj.get_full_name()
        return full if full else obj.username


class BoardTaskSerializer(serializers.ModelSerializer):
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

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
            'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'members',
            'owner_id',
            'tasks',
        ]

    def get_tasks(self, obj):
        tasks = obj.tasks.all().select_related(
            'assignee',
            'reviewer'
        )
        return BoardTaskSerializer(tasks, many=True).data


class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Board
        fields = [
            'title',
            'members',
        ]

    def update(self, instance, validated_data):
        if "title" in validated_data:
            instance.title = validated_data["title"]

        if "members" in validated_data:
            new_members = validated_data["members"]

            owner = instance.owner
            if owner not in new_members:
                new_members.append(owner)

            instance.members.set(new_members)

        instance.save()
        return instance


class BoardOwnerSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'fullname'
        ]

    def get_fullname(self, obj):
        full = obj.get_full_name()
        return full if full else obj.username


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = BoardOwnerSerializer(source='owner', read_only=True)
    members_data = BoardMemberSerializer(
        source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_data',
            'members_data',
        ]
