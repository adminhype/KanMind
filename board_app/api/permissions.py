from rest_framework import permissions


class IsBoardOwnerOrMember(permissions.BasePermission):
    """
    allow acces if user is owner or member of the board.
    required for GET /api/boards/{id}/ and PATCH.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or user in obj.members.all()


class isOwnerOnly(permissions.BasePermission):
    """
    allows acces only if user is the owner.
    required for delete action.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
