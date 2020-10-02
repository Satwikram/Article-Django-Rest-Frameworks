from rest_framework import serializers
from .models import ArticleGen

class ArticleGenSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArticleGen
        fields = [
            'id',
            'title',
            'author',
            'email',
            'time',
            'text',
            'date'
         ]
