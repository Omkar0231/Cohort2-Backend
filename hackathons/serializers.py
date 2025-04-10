from rest_framework import serializers
from .models import Hackathon, HackathonApplication

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'

class ApplyHackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonApplication
        fields = ['hackathon']
