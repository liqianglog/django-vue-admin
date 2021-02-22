from rest_framework import serializers

from apps.permission.models import UserProfile


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'username',)
