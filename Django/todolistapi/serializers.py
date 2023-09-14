from rest_framework import serializers
from .listmodel import task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = task
        fields = ('id', 'title', 'description', 'completed')