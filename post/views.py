from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from pusher_push_notifications import PushNotifications
from .models import Article, Comment
from .serializers import ArticleSerializers, CommentSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from article.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string, get_template
from django.template import Context


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


def push_notify(comment):
    """
    beams_client = PushNotifications(
        instance_id='YOUR_INSTANCE_ID_HERE',
        secret_key='YOUR_SECRET_KEY_HERE',
    )

    response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={
            'apns': {
                'aps': {
                    'alert': 'Someone Commented'
                }
            },
            'fcm': {
                'notification': {
                    'title': 'Hello',
                    'body': str(comment)
                }
            }
        }
    )
    """
    subject = 'Commented!'
    recepient = 'kushal.h1999@gmail.com'
    body = str(comment)
    print(body)

    send_mail(subject, body, EMAIL_HOST_USER, [recepient], fail_silently=False)

    #print(response['publishId'])

class CommentAPIView(APIView):

    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializers(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            push_notify(serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class APIArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'author', 'text')

