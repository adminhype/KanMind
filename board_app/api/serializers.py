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
