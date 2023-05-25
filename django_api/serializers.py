from rest_framework import serializers
from .models import Post, Comment, CommentLike, PostLike
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    post = serializers.ReadOnlyField(source='post.post_id')

    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'body', 'created_on', 'user', 'user_id', 'user_email']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'post_id', 'title', 'body', 'user', 'user_id', 'user_email',
            'created_on', 'comments', 'comment_count', 'likes', 'image'
        ]

    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_likes(self, post):
        return PostLike.objects.filter(post=post).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['postlike_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # User an existing Django user model
        model = User
        # We only care about username and password
        fields = ('username', 'password')
        # Do not allow the password to be read cia the API
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # We override this function only because we want to store the password safely
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
