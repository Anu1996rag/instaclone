from django.http import HttpResponse
from django.db.models import Count, F
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer
from .serializers import NetworkEdgeCreationSerializer, NetworkEdgeViewFollowingSerializer, \
    NetworkEdgeViewFollowerSerializer, UserProfileListViewSerializer
from .models import UserProfile, NetworkEdge

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets


def get_default_response():
    return {
        "errors": None or "",
        "data": None or ""
    }


# Create your views here.
def index(request):
    return HttpResponse("Congratulations for your first view implementation !!!")


@swagger_auto_schema(methods=['post'], request_body=UserCreateSerializer)
@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)

    resp_data = get_default_response()

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        resp_data["data"] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        resp_status = status.HTTP_201_CREATED
    else:
        resp_data["errors"] = serializer.errors
        resp_status = status.HTTP_400_BAD_REQUEST

    return Response(resp_data, status=resp_status)


class ListUsers(viewsets.GenericViewSet,
                mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        users = UserProfile.objects.all().select_related('user').annotate(
            follower_count=Count('followers', distinct=True),
            following_count=Count('following', distinct=True)
        )

        serialized_data = UserProfileListViewSerializer(instance=users, many=True)

        return Response(
            data=serialized_data.data,
            status=status.HTTP_200_OK
        )


@swagger_auto_schema(request_body=UserProfile)
class UserProfileDetail(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = UserProfile.objects.all()

    def retrieve(self, request, pk=None):
        resp_data = get_default_response()

        user = self.queryset.filter(id=pk).select_related('user').first()

        if user:
            serialized_data = UserProfileViewSerializer(instance=user)
            resp_data["data"] = serialized_data.data
            resp_status = status.HTTP_200_OK
        else:
            resp_data["errors"] = "Requested user does not exists"
            resp_status = status.HTTP_404_NOT_FOUND

        return Response(
            data=resp_data,
            status=resp_status
        )

    @swagger_auto_schema(request_body=UserProfileUpdateSerializer)
    def update(self, request, pk):
        resp_data = get_default_response()

        user_profile_serializer = UserProfileUpdateSerializer(instance=request.user.profile,
                                                              data=request.data)

        if user_profile_serializer.is_valid():
            user_profie = user_profile_serializer.save()

            resp_data["data"] = UserProfileViewSerializer(instance=user_profie).data
            resp_status = status.HTTP_200_OK
        else:
            resp_data["errors"] = user_profile_serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST

        return Response(data=resp_data["data"],
                        status=resp_status)


class UserNetworkEdgeView(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            edge_direction = self.request.query_params.get("direction")
            if edge_direction == "followers":
                return NetworkEdgeViewFollowerSerializer
            elif edge_direction == "following":
                return NetworkEdgeViewFollowingSerializer

        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        edge_direction = self.request.query_params.get("direction")
        if edge_direction == "followers":
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == "following":
            return self.queryset.filter(from_user=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data["from_user"] = request.user.profile.id

        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile,
                                                  to_user=request.data["to_user"])

        if network_edge.exists():
            network_edge.delete()
            message = "User unfollowed"
        else:
            message = "User not found"

        return Response(data={
            "data": None,
            "message": message
        }, status=status.HTTP_200_OK)
