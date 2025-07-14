from django.db import models
from gdg_be.users.models import User


# Create your models here.
class Resource(models.Model):
    interest = models.CharField(max_length=255)
    description = models.TextField()
    domain = models.CharField(max_length=255, default="general")
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    domain = models.CharField(max_length=255, default="general")
    type = models.CharField(max_length=255, default="default")
    level = models.CharField(max_length=255, default="beginner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    project = models.ForeignKey(Project, related_name="steps", on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProject(models.Model):
    user = models.ForeignKey(
        User, related_name="user_projects", on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, related_name="user_projects", on_delete=models.CASCADE
    )
    current_step = models.ForeignKey(
        Step,
        related_name="user_projects",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "project")
        # Or, for Django 2.2+:
        # constraints = [
        #     models.UniqueConstraint(fields=["user", "project"], name="unique_user_project")
        # ]

    def __str__(self):
        return self.project.name
