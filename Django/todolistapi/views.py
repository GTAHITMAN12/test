from django.shortcuts import render
from .serializers import TaskSerializer
from .listmodel import task
from rest_framework import generics

class TaskListCreate(generics.ListCreateAPIView):
    queryset = task.objects.all()
    serializer_class = TaskSerializer
    
class TaskDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = task.objects.all()
    serializer_class = TaskSerializer