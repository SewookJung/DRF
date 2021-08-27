from django.http import HttpResponse
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from django.shortcuts import get_object_or_404


from .models import Article
from .serializers import ArticleSerializer


class GenericViewSet(ViewSet):
    def list(self, request):
        qs = Article.objects.all()
        serializer = ArticleSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        qs = Article.objects.all()
        article = get_object_or_404(qs, pk)
        serializer = ArticleSerializer(data=request.data)
        return Response(serializer.data)


# Generic view and mixins
class GenericApiView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


# Class base views
class ArticleApiView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetails(APIView):
    def get_object(self, pk):
        try:
            article = Article.objects.get(pk=pk)
            return article
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk=pk)
        article.delete()
        return Response(status.HTTP_204_NO_CONTENT)


# Funciton base vuew
@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        article.delete()
        return Response(status.HTTP_204_NO_CONTENT)
