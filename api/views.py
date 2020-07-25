from django.shortcuts import render
from rest_framework import status,filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.serializers import ContentSerializer
from .models import Content
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrAuthor


class CreateView(ListCreateAPIView):
  search_fields = ['title','body','summary']
  filter_backends = (filters.SearchFilter,)
  serializer_class = ContentSerializer
  queryset = Content.objects.all()
  permission_classes = (IsAuthenticated,IsAdminOrAuthor,)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class DetailView(RetrieveUpdateDestroyAPIView):
  serializer_class = ContentSerializer
  queryset = Content.objects.all()
  permission_classes = (IsAuthenticated,IsAdminOrAuthor,)


# @api_view(['GET','PUT','DELETE'])
# def get_delete_update_content(request,pk):
#   try:
#     content = Content.objects.get(pk=pk)
#   except:
#     return Response(status=status.HTTP_404_NOT_FOUND)
#   if request.method == 'GET':
#     serializer = ContentSerializer(content)
#     return Response(serializer.data)
#   if request.method == 'PUT':
#     serializer = ContentSerializer(content,data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data,status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_400_BAD_REQUEST)
#   if request.method == 'DELETE':
#     content.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
  
  
# @api_view(['GET','POST'])
# def get_post_content(request):
#   if request.method == 'GET':
#     content = Content.objects.all()
#     serializer = ContentSerializer(content,many=True)
#     return Response(serializer.data)
#   if request.method == 'POST':
#     data = {
#       'title':request.data.get("title"),
#       'body':request.data.get("body"),
#       'summary':request.data.get("summary"),
#     }
#     serializer = ContentSerializer(data=data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(status=status.HTTP_400_BAD_REQUEST)