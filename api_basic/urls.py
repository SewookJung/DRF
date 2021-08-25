from django.urls import path
from .views import article_list, article_detail, ArticleApiView, ArticleDetails

urlpatterns = [
    path("article/", ArticleApiView.as_view()),
    path("article/<int:pk>/", ArticleDetails.as_view()),
]
