from django.contrib import admin
from .models import PostComments, PostLikes, UserPost


class UserPostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_display = ('id', 'caption_text', 'created_on', 'updated_on',)
    list_filter = ('created_on',)


class PostLikesAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_filter = ('created_on',)
    list_display = ('id', 'get_post_by', 'get_caption', 'get_author')

    @admin.display(description='Author')
    def get_author(self, obj):
        return obj.liked_by.user

    @admin.display(description='Post By')
    def get_post_by(self, obj):
        return obj.post.author.user

    @admin.display(description='Post')
    def get_caption(self, obj):
        return obj.post.caption_text


class PostCommentsAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"
    list_filter = ('created_on',)
    list_display = ('id', 'get_post', 'get_author', 'text', )

    @admin.display(description='Post')
    def get_post(self, obj):
        return obj.post.caption_text

    @admin.display(description='Author')
    def get_author(self, obj):
        return obj.author.user




# Register your models here.
admin.site.register(PostLikes, PostLikesAdmin)
admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(UserPost, UserPostAdmin)
