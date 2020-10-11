from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'author',
            'email',
            'time',
            'slug',
            'text',
            'date'
         ]

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'comment'
        ]