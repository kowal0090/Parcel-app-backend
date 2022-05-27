from rest_framework import serializers
from api.serializers.note import NoteSerializer
from api.models import Project, Parcel
from django.db.models import Count


# class ParcelGeomWktSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         return super().to_representation(instance)['geom_wkt']
#
#     class Meta:
#         model = Parcel
#         fields = ("geom_wkt",)

# parcels_geom = ParcelGeomWktSerializer(source="parcels", many=True)
# parcels_geom = serializers.SerializerMethodField()

# def get_parcels_geom(self, project):
#     parcels_geom = Parcel.objects.filter(project=project)
#     return ParcelGeomWktSerializer(parcels_geom, many=True).data

# parcels_geom = ParcelGeomWktSerializer(source="parcels", many=True)

class PostPutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "color")


class ParcelMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ("id", "identifier", "voivodeship", "county", "commune", "region", "parcel_num", "geom_wkt")


class ProjectOutputSerializer(serializers.ModelSerializer):
    parcels_count = serializers.IntegerField()
    parcels = ParcelMiniSerializer(many=True)

    class Meta:
        model = Project
        fields = ("id", "title", "description", "created_at", "parcels_count", "color", "parcels")


class GetProjectDetailsSerializer(serializers.ModelSerializer):
    parcels = ParcelMiniSerializer(many=True)
    notes = NoteSerializer(many=True)
    parcels_count = serializers.SerializerMethodField(read_only=True)

    def get_parcels_count(self, obj):
        return obj.parcels.count()

    class Meta:
        model = Project
        fields = ("id", "title", "description", "created_at", "color", "parcels_count",  "notes", "parcels", )



