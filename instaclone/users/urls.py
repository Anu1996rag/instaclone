from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('index/', views.index, name="users_first_view"),
    path('add/', views.create_user, name="create_user_api"),
    path('login/', TokenObtainPairView.as_view(), name='login_api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('list/', views.ListUsers.as_view(), name="list_users_api"),
    path('<int:pk>/', views.UserProfileDetail.as_view(), name="get_single_user_api"),
    path('edge/', views.UserNetworkEdgeView.as_view(), name="user_network_edge_api"),
]