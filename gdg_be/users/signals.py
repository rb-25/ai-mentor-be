from django.db.models.signals import post_save
from django.dispatch import receiver
from gdg_be.users.models import User
from gdg_be.core.models import Project, UserProject


@receiver(post_save, sender=User)
def create_user_projects_for_interests(sender, instance, created, **kwargs):
    if created:
        interests = instance.interests or []
        for interest in interests:
            default_projects = Project.objects.filter(domain=interest, type="default")
            for project in default_projects:
                UserProject.objects.get_or_create(user=instance, project=project)
