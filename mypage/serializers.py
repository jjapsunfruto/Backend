from rest_framework import serializers

from User.models import User, House

class UserInfoSerializer(serializers.ModelSerializer):
    userid = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model=User
        fields=['userid', 'nickname', 'userCharacter']

class HouseInfoSerializer(serializers.ModelSerializer):
    #housecode = serializers.IntegerField()
    class Meta:
        model=House
        fields=['housename', 'housecode']

class HouseMemberSerializer(serializers.ModelSerializer):
    userid = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = User
        fields = ['userid', 'nickname', 'userCharacter']

class RemoveMemberSerializer(serializers.Serializer):
    userid = serializers.IntegerField(source="id", read_only=True)