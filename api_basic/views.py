from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Article
from .serializers import ArticleSerializer


@csrf_exempt
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        else:
            return JsonResponse(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )


@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:
            return JsonResponse(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )

    elif request.method == "DELETE":
        article.delete()
        return HttpResponse(status.HTTP_204_NO_CONTENT)
