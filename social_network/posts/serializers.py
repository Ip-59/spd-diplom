from rest_framework import serializers
from .models import Post, Comment, Like, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    # Для записи картинок используем отдельное поле
    new_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    location_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'text', 'created_at', 'comments', 'likes_count',
            'images', 'new_images', 'location_name', 'latitude', 'longitude'
        ]
        read_only_fields = ['id', 'created_at', 'comments', 'likes_count', 'images']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        images_data = validated_data.pop('new_images', [])
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, image=image_data)
        return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('new_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for image_data in images_data:
            PostImage.objects.create(post=instance, image=image_data)
        return instance