from django.urls import path
from .views import *

urlpatterns = [
        path('article/', article_list),


]
