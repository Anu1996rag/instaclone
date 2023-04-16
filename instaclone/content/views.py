from django.shortcuts import render
from .models import UserPost
from .serializers import UserPostCreateSerializer, PostMediaCreateSerializer,\
    PostFeedSerializer, PostMediaViewSerializer
from .filters import CurrentUserFollowingFilterBackend, IsPublishedUserFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics
from rest_framework import mixins


# Create your views here.
class UserPostCreateFeed(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = UserPost.objects.all()
    filter_backends = [CurrentUserFollowingFilterBackend, ]
    serializer_class = UserPostCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostFeedSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostMediaView(generics.GenericAPIView,
                    mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = PostMediaCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserPostDetailUpdateView(generics.GenericAPIView,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer
    queryset = UserPost.objects.all()
    filter_backends = [IsPublishedUserFilterBackend, ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostFeedSerializer
        return self.serializer_class

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
