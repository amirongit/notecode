from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt  # Allow post requests from clients who don't have a csrf token.
def non_drf_snippet_list(request):
    '''
    List all code snippets, or create a new snippet.
    '''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def non_drf_snippet_detail(request, pk):
    '''
    Retrieve, update or delete a code snippet.
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


# Django REST framework provides Request and Response classes which are
# extended versions of the same classes in django.
# DRF's request objects has the data attribute which is capable of returning
# data in the request, without paying attention to the request's method,
# whereas django's version of request objects only has the POST attribute to
# retrieve data. Using the data attribute, it isn't necessary to parse the
# incoming data.
# DRF's response objects are capable of taking the unrendered data, and finding
# out in which content type the data should be returned to the client.
# DRF also provides a status module to use status codes with better
# identifiers.
# There are 2 wrappers present in DRF to be used for writing API views, one for
# class-based views and the other one for function-based views. These wrappers
# make sure that you get the DRF version of request objects, and add context to
# the outgoing response so it can find the suitable content type. They also
# handle parse errors and expose some other behaviours.


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    '''
    List all code snippets, or create a new snippet.
    '''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    '''
    Retrieve, update or delete a code snippet.
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
