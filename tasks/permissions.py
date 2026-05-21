from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission that grants access only to the task's
    owner or to users with the admin role.

    - Regular users: can only read/modify/delete their own tasks.
    - Admin users: can access any task regardless of ownership.

    Applied on detail endpoints (GET/PUT/PATCH/DELETE /tasks/:id/).
    List-level filtering is handled separately in the view's get_queryset().
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_admin()