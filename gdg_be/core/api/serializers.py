from rest_framework import serializers

from gdg_be.core.models import Resource, Project, Step, UserProject


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"


class UserProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    project_description = serializers.CharField(
        source="project.description", read_only=True
    )
    project_domain = serializers.CharField(source="project.domain", read_only=True)
    steps = serializers.SerializerMethodField()

    class Meta:
        model = UserProject
        fields = [
            "id",
            "user",
            "project",
            "project_name",
            "project_description",
            "project_domain",
            "steps",
            "current_step",
            "is_started",
            "is_completed",
            "created_at",
            "updated_at",
        ]

    def get_steps(self, obj):
        """Get all steps for the project"""
        steps = Step.objects.filter(project=obj.project)
        return StepSerializer(steps, many=True).data
