from rest_framework import serializers
from .models import Resident, Visitor, Guard, Vehicle


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = '__all__'


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'


class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'