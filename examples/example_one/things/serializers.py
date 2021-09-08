from rest_framework import serializers

from .models import Property, Thing


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
