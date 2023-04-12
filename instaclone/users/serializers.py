from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import UserProfile, NetworkEdge


class UserCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        user = User.objects.create(**validated_data)

        UserProfile.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserViewSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserProfileViewSerializer(ModelSerializer):
    user = UserViewSerializer()

    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = UserProfile
        exclude = ('id', 'is_verified',)


class UserProfileUpdateSerializer(ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):
        user = instance.user

        user.first_name = validated_data.pop('first_name', None)
        user.last_name = validated_data.pop('last_name', None)

        user.save()

        instance.bio = validated_data.get('bio', None)
        instance.profile_pic_url = validated_data.get('profile_pic_url', None)

        instance.save()

        return instance

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'profile_pic_url', )


class NetworkEdgeCreationSerializer(ModelSerializer):
    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user', )


class NetworkEdgeViewFollowingSerializer(ModelSerializer):
    from_user = UserProfileViewSerializer()

    class Meta:
        model = UserProfile
        fields = ("from_user", )


class NetworkEdgeViewFollowerSerializer(ModelSerializer):
    to_user = UserProfileViewSerializer()

    class Meta:
        model = UserProfile
        fields = ("to_user", )
