from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Article, Comment
from .serializers import ArticleSerializers, CommentSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializers(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ArticleDetailsAPIView(APIView):

    def get_object(self, id):
        try:
            article = Article.objects.get(id = id)
            comment = Comment.objects.filter(post_id = id)
            print(len(comment))
            n = len(comment)
            comment1 = list(Comment.objects.filter(post_id = id).values('comment'))
            print("Comment is:",comment)
            print("Comment is:", comment1)
            print("Article is:",article)
            return article, comment1

        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            article, comment1 = self.get_object(id)
            serializer = ArticleSerializers(article)
            print("Its worked")
            return Response({
                'post':serializer.data,
                'comment': comment1
            })
        except:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)


    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializers(article, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CommentAPIView(APIView):

    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializers(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
