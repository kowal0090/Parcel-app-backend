from api.models import Project
from rest_framework import viewsets
from api.serializers.project import ProjectOutputSerializer, GetProjectDetailsSerializer, PostPutProjectSerializer
from rest_framework.response import Response
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_classes = {
        'retrieve': GetProjectDetailsSerializer,
        'create': PostPutProjectSerializer,
        'update': PostPutProjectSerializer,
    }
    default_serializer_class = None
    pagination_class = None
    http_method_names = ['get', "post", "delete", "put"]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        projects = Project.objects.annotate(parcels_count=Count('parcels')).order_by("-created_at")
        serialized = ProjectOutputSerializer(projects, many=True)
        return Response(serialized.data)

    @swagger_auto_schema(responses={200: ProjectOutputSerializer()})
    def update(self, request, *args, **kwargs):
        serializer = PostPutProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.get_object()
        project.parcels_count = project.parcels.count()
        for k, v in serializer.validated_data.items():
            setattr(project, k, v)
        project.save()

        serialized = ProjectOutputSerializer(project, many=False)
        return Response(serialized.data, status=200)

    @swagger_auto_schema(responses={201: ProjectOutputSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = PostPutProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = Project.objects.create(**serializer.validated_data)
        project.parcels_count = 0
        serialized = ProjectOutputSerializer(project, many=False)
        return Response(serialized.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = GetProjectDetailsSerializer(project)
        return Response(serializer.data, status=200)





    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serialized = ProjectMiniSerializer(instance)
    #     return Response(serialized.data)

    # def create(self, request, *args, **kwargs):
    #     name = request.data['name']
    #     project = Project.objects.create(name=name)
    #     project.save()
    #     serialized = ProjectSerializer(project, many=False)
    #     return Response(serialized.data)

    # def update(self, request, *args, **kwargs):
    #     project = self.get_object()
    #     project.name = request.data['name']
    #     project.save()
    #     serialized = ProjectSerializer(project, many=False)
    #     return Response(serialized.data)

    # def destroy(self, request, *args, **kwargs):
    #     project = self.get_object()
    #     project.delete()
    #     return Response("project deleted")

    # @action(detail=False, methods=["post"], serializer_class=UpdateAllSerializer)
    # def update_all(self, request, *args, **kwargs):
    #     projects = Project.objects.all()
    #     projects.update(note=request.data['note'])
    #     serialized = ProjectSerializer(projects, many=True)
    #     return Response(serialized.data)








