from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = DefaultRouter()
router.register('list', views.ListUsers, basename="list_test_api")
router.register('', views.UserProfileDetail, basename="single_user_api")


urlpatterns = [
    path('index/', views.index, name="users_first_view"),
    path('add/', views.create_user, name="create_user_api"),
    path('login/', TokenObtainPairView.as_view(), name='login_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('edge/', views.UserNetworkEdgeView.as_view(), name="user_network_edge_api"),
    path('', include(router.urls)),
]