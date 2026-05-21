from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/tasks/   — List tasks for the current user.
    POST /api/v1/tasks/   — Create a new task owned by the current user.

    Admins receive all tasks across all users.
    Regular users receive only their own tasks.

    Supports:
        - ?search=<query>  filters by title or status
        - ?ordering=created_at or ?ordering=status
    """
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title', 'status']
    ordering_fields    = ['created_at', 'status']

    def get_queryset(self):
        # Admins see all tasks; regular users see only their own
        if self.request.user.is_admin():
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user as the task owner
        when saving. The owner field is never taken from request data.
        """
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/tasks/:id/  — Retrieve a single task.
    PUT    /api/v1/tasks/:id/  — Full update of a task.
    PATCH  /api/v1/tasks/:id/  — Partial update (e.g. status only).
    DELETE /api/v1/tasks/:id/  — Delete a task.

    Access is restricted by IsOwnerOrAdmin — only the task's owner
    or an admin can perform these operations. Returns 403 otherwise.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_admin():
            return Task.objects.all()
        
        return Task.objects.filter(owner = self.request.user)