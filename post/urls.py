from django.urls import path
from .views import *

urlpatterns = [
        #path('article/', article_list),
        path('article/', ArticleAPIView.as_view()),
        path('detail/<int:id>/', ArticleDetailsAPIView.as_view())
        #path('detail/<int:id>/', article_detail),


]
