from rest_framework import serializers

from User.models import User, HouseworkTag
from .models import Housework
from User.serializers import UserHouseworkSerializer

class HouseworkTagSerializer(serializers.Serializer):
    tagid = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = HouseworkTag
        fields = ['tagid', 'tag']

class HouseworkSerializer(serializers.ModelSerializer):
    user=UserHouseworkSerializer(read_only=True)
    tag=HouseworkTagSerializer(read_only=True)
    houseworkDone=False

    class Meta:
        model = Housework
        fields = ['houseworkId', 'user', 'tag', 'houseworkDate', 
                  'houseworkPlace', 'houseworkDetail', 'houseworkDone']