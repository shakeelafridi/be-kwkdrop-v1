from utilities.models import kwkChargesStructure
from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers



class GetChargesStructureSerialzer(serializers.ModelSerializer):
    class Meta:
        model = kwkChargesStructure
        fields = '__all__'