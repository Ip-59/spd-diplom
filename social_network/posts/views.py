from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from geopy.geocoders import Nominatim

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        location_name = self.request.data.get('location_name')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        # Если есть название места, получить координаты через geopy
        if location_name and (not latitude or not longitude):
            geolocator = Nominatim(user_agent="social_network")
            location = geolocator.geocode(location_name)
            if location:
                latitude = location.latitude
                longitude = location.longitude
        # Если есть координаты, получить название объекта
        elif latitude and longitude and not location_name:
            geolocator = Nominatim(user_agent="social_network")
            location = geolocator.reverse((latitude, longitude))
            location_name = location.address if location else None

        serializer.save(
            author=self.request.user,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

    def perform_update(self, serializer):
        # Логика аналогична create
        self.perform_create(serializer)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Вы уже поставили лайк.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Лайк поставлен.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({'detail': 'Лайк удалён.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Лайка не было.'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        serializer.save(author=self.request.user, post_id=post_id)