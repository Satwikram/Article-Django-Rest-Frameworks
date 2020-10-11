from django.urls import path
from .views import *

urlpatterns = [
                path('generic/article', GenericAPIView.as_view()),
]