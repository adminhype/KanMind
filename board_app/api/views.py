from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from board_app.models import Board
from .serializers import BoardDetailSerializer, BoardSerializer, BoardUpdateSerializer, BoardUpdateResponseSerializer
from .permissions import IsBoardOwnerOrMember


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated, IsBoardOwnerOrMember]
        return [perm() for perm in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action in ['update', 'partial_update']:
            return BoardUpdateSerializer
        return BoardSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        update_board = serializer.save()

        response_serializer = BoardUpdateResponseSerializer(update_board)
        return Response(response_serializer.data)

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Only the owner can delete this board.")
        return super().perform_destroy(instance)
