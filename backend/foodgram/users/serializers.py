from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

CustomUser = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        if request:
            requested_user = request.user
        return author.following.filter(
            user=requested_user
        ).exists()
