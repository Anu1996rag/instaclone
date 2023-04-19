from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import APIException
from .models import UserPost, PostMedia, PostLikes
from users.serializers import UserProfileViewSerializer


class UserPostCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["author"] = self.context["current_user"]

        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ('caption_text', 'location', 'id', 'is_published',)


class PostMediaCreateSerializer(ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post',)


class PostMediaViewSerializer(ModelSerializer):
    class Meta:
        model = PostMedia
        exclude = ('post',)


class PostFeedSerializer(ModelSerializer):
    author = UserProfileViewSerializer()
    media = PostMediaViewSerializer(many=True)

    class Meta:
        model = UserPost
        fields = "__all__"
        include = ('media_file',)


class PostLikeCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["liked_by"] = self.context["current_user"]
        try:
            return PostLikes.objects.create(**validated_data)
        except IntegrityError as error:
            raise APIException(detail=error)

    class Meta:
        model = PostLikes
        fields = ('id', 'post',)


class PostLikeViewSerializer(ModelSerializer):
    liked_by = UserProfileViewSerializer()

    class Meta:
        model = PostLikes
        fields = ('id', 'post', 'liked_by', )
