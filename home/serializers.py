from rest_framework import serializers
from User.models import User
from Housework.models import Housework
from KKaebiBack.utils import (
    calculate_today_completion_rate,
    calculate_weekly_completion_rate,
    calculate_level
)
from datetime import date, timedelta


class UserSerializer(serializers.ModelSerializer):
    today_completion_rate = serializers.SerializerMethodField()
    weekly_completion_rate = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['nickname', 'userCharacter', 'today_completion_rate', 'weekly_completion_rate', 'level']

    def get_today_completion_rate(self, user):
        today_tasks = Housework.objects.filter(user=user, houseworkDate=date.today())
        if not today_tasks.exists():
            return "none"
        return f"{calculate_today_completion_rate(user)}%"

    def get_weekly_completion_rate(self, user):
        return f"{calculate_weekly_completion_rate(user)}%"

    def get_level(self, user):
        return calculate_level(calculate_weekly_completion_rate(user))
    

class HouseworkSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag.tag', allow_null=True)

    class Meta:
        model = Housework
        fields = ['houseworkId', 'tag', 'houseworkDate', 'houseworkPlace', 'houseworkDetail', 'houseworkDone']




class DistributionSerializer(serializers.ModelSerializer):
    total_tasks = serializers.SerializerMethodField()
    distribution_percentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['nickname', 'total_tasks', 'distribution_percentage']

    def get_total_tasks(self, user):
        houseworks = self.context['houseworks']
        return houseworks.filter(user=user).count()

    def get_distribution_percentage(self, user):
        houseworks = self.context['houseworks']
        member_tasks = houseworks.filter(user=user).count()
        if member_tasks == 0:
            return "none"
        completed_tasks = houseworks.filter(user=user, houseworkDone=True).count()
        return f"{int((completed_tasks / member_tasks) * 100)}%"



class HouseStatsSerializer(serializers.Serializer):
    house_completion_rate = serializers.SerializerMethodField()
    distribution = serializers.SerializerMethodField()

    def get_house_completion_rate(self, obj):
        houseworks = obj['houseworks']
        total_tasks = houseworks.count()
        if total_tasks == 0:
            return "none"
        completed_tasks = houseworks.filter(houseworkDone=True).count()
        return f"{int((completed_tasks / total_tasks) * 100)}%"

    def get_distribution(self, obj):
        members = obj['members']
        houseworks = obj['houseworks']
        return DistributionSerializer(members, many=True, context={'houseworks': houseworks}).data
