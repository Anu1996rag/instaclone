from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('like', views.PostLikeViewSet)
router.register('comment', views.PostCommentViewSet)

urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name="user_post_view"),
    path('media/', views.PostMediaView.as_view(),name="post_media_view"),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name="user_post_detail_update"),
    path('', include(router.urls)),
]