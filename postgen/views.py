from django.shortcuts import render
from .models import ArticleGen
from .serializers import ArticleGenSerializers
from rest_framework import generics, mixins

# Create your views here.

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ArticleGenSerializers
    queryset = ArticleGen.objects.all()

    def get(self, request, id):
        return self.list(request)


