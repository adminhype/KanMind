from rest_framework import serializers

from django.contrib.auth.models import User

from board_app.models import Board


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
        # todo: customize (z.B. obj.tasks.count())
        return 0

    def get_tasks_to_do_count(self, obj):
        # todo: customize (obj.tasks.count())
        return 0

    def get_tasks_high_prio_count(self, obj):
        # todo: customize (obj.tasks.count())
        return 0


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
        # Dummy data for illustration; replace with actual task serialization
        return [
            {
                "id": 5,
                "title": "API-Dokumentation schreiben",
                "description": "Die API-Dokumentation für das Backend vervollständigen",
                "status": "to-do",
                "priority": "high",
                "assignee": None,
                "reviewer": {
                    "id": 1,
                    "email": "max.mustermann@example.com",
                    "fullname": "Max Mustermann"
                },
                "due_date": "2025-02-25",
                "comments_count": 0
            },
            {
                "id": 8,
                "title": "Code-Review durchführen",
                "description": "Den neuen PR für das Feature X überprüfen",
                "status": "review",
                "priority": "medium",
                "assignee": {
                    "id": 1,
                    "email": "max.mustermann@example.com",
                    "fullname": "Max Mustermann"
                },
                "reviewer": None,
                "due_date": "2025-02-27",
                "comments_count": 0
            }
        ]
