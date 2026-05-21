from django.db import models
from django.conf import settings
# Create your models here.

class Task(models.Model):
    """
    Represents a task owned by a user.

    Attributes:
        owner (User): The user who created and owns this task.
        title (str): Short label for the task (max 255 chars).
        description (str): Optional longer description.
        status (str): Current state — pending, in_progress, or done.
        created_at (datetime): Timestamp set on creation.
        updated_at (datetime): Timestamp updated on every save.
    """
    class Status(models.TextChoices):
        """Valid status values for a task."""
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    