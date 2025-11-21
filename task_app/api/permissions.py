from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):
    """
    allow acces only to member of the board linked to task.
    """

    def has_object_permission(self, request, view, obj):
        # obj is the task instance
        return request.user in obj.board.members.all() or request.user == obj.board.owner


class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    """
    allow delete only for task creator or board owner.
    """

    def has_object_permission(self, request, view, obj):
        is_creator = obj.creator == request.user
        is_board_owner = obj.board.owner == request.user
        return is_creator or is_board_owner


class IsCommentAuthor(permissions.BasePermission):
    """
    allow delete only for the author of the comment.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
