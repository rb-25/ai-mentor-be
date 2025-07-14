from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from gdg_be.users.authentication import FirebaseAuthentication
from gdg_be.users.models import User
import os
import google.generativeai as genai
import json

from gdg_be.core.models import Resource, Project, Step, UserProject
from gdg_be.core.api.serializers import (
    ResourceSerializer,
    ProjectSerializer,
    StepSerializer,
    UserProjectSerializer,
)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        description = request.data.get("description")
        domain = request.data.get("domain")
        project = Project.objects.create(
            name=name, description=description, domain=domain
        )
        response = model.generate_content(
            contents=f"Generate a list of steps for a project with the following name: {name} and the following description: {description}. They are working in the following domain: {domain}. Return the steps as a list of dictionaries in a json format with the following fields: name, description, deadline, is_completed. Here is an example of the json format: [ {{'name': 'Step Name 1', 'description': 'Step Description 1', 'deadline': '1 Week', 'is_completed': False}}, {{'name': 'Step Name 2', 'description': 'Step Description 2', 'deadline': '1 Weeks', 'is_completed': False}}, {{'name': 'Step Name 3', 'description': 'Step Description 3', 'deadline': '2 Weeks', 'is_completed': False}}, {{'name': 'Step Name 4', 'description': 'Step Description 4', 'deadline': '3 Weeks', 'is_completed': False}}, {{'name': 'Step Name 5', 'description': 'Step Description 5', 'deadline': '5 Weeks', 'is_completed': False}}, ..... and so on]. The deadline should be set according to the difficulty of the step. Make sure that you dont specify any language in the description or return any code snippets, it should be a list of steps that are relevant to the project and the domain. Also the description should be detailed and start from the basics. This is for someone who is trying to learn {domain}. Do not include ```json or ```python in the response. It should start directly with the list.",
        )
        print(response.text)
        try:
            if response.text.startswith("```json"):
                response.text = response.text[7:]
            if response.text.endswith("```"):
                response.text = response.text[:-3]
            steps = json.loads(response.text)  # Parse the string to a Python list
        except json.JSONDecodeError as e:
            return Response(
                {"error": "Invalid JSON from model", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for step in steps:
            step["project"] = project.id
            serializer = StepSerializer(data=step)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        UserProject.objects.create(user=request.user, project=project)
        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)


class StepViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class UserProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        project = Project.objects.get(id=request.data.get("project"))
        step = Step.objects.filter(project=project, ordering=1).first()
        user_project = UserProject.objects.create(
            user=user, project=project, is_started=True, current_step=step
        )
        return Response(
            UserProjectSerializer(user_project).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        user_project = UserProject.objects.get(id=kwargs.get("id"))
        if request.data.get("is_started") and user_project.is_started == False:
            user_project.is_started = True
        if request.data.get("is_completed") and user_project.is_completed == False:
            user_project.is_completed = True
        if request.data.get("current_step"):
            project = user_project.project
            step = Step.objects.filter(
                project=project, ordering=int(request.data.get("current_step")) + 1
            ).first()
            user_project.current_step = step
        user_project.save()
        return Response(
            UserProjectSerializer(user_project).data, status=status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):
        user = request.user
        user_projects = UserProject.objects.filter(user=user)
        return Response(
            UserProjectSerializer(user_projects, many=True).data,
            status=status.HTTP_200_OK,
        )


class NewProjectView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        response = model.generate_content(
            contents=f"Generate a list of 5 projects for a user with the following interests: {user.interests} and the following experience: {user.experience}. Make sure the project isnt any of the following: {UserProject.objects.filter(user=user).values_list('project__name', flat=True)}. Return the project as a list of dictionaries in a json format with the following fields: name, description, is_started, is_completed. Here is an example of the json format: [ {{'name': 'Project Name 1', 'description': 'Project Description 1', 'is_started': False, 'is_completed': False}}, {{'name': 'Project Name 2', 'description': 'Project Description 2', 'is_started': False, 'is_completed': False}}, {{'name': 'Project Name 3', 'description': 'Project Description 3', 'is_started': False, 'is_completed': False}}, {{'name': 'Project Name 4', 'description': 'Project Description 4', 'is_started': False, 'is_completed': False}}, {{'name': 'Project Name 5', 'description': 'Project Description 5', 'is_started': False, 'is_completed': False}}]",
        )
        for project in response.text:
            serializer = ProjectSerializer(data=project)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.text, status=status.HTTP_200_OK)
