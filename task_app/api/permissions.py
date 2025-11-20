from rest_framework import permissions


class TaskPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user not in obj.board.members.all():
            return False
        if request.method == 'DELETE':
            is_creator = (obj.creator == request.user)
            is_board_owner = (obj.board.owner == request.user)
            return is_creator or is_board_owner
        return True


class IsCommentAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
