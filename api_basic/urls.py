from django.urls import path
from .views import (
    article_list,
    article_detail,
    ArticleApiView,
    ArticleDetails,
    GenericApiView,
)

urlpatterns = [
    path("article/", ArticleApiView.as_view()),
    path("article/<int:pk>/", ArticleDetails.as_view()),
    path("generic/article/<int:pk>/", GenericApiView.as_view()),
]
