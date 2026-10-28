from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView

from . models import Project

# Create your views here.


class ProjectListCreateView(ListCreateAPIView):

    queryset = Project.objects.filter(active_status=True)

    serializer_class = ''