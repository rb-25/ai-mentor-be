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
    project = ProjectSerializer()

    class Meta:
        model = UserProject
        fields = "__all__"
