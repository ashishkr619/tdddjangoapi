from rest_framework import serializers
from .models import Content


class ContentSerializer(serializers.ModelSerializer):

  owner = serializers.ReadOnlyField(source='owner.email')

  class Meta:
    model = Content
    fields = ('id','title','owner','body','summary')
    
