from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from notifications.models import Notification
from django.shortcuts import get_object_or_404




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupère les utilisateurs que l'utilisateur connecté suit
        following_users = request.user.following.all()

        # Récupère les posts de ces utilisateurs, triés par date de création décroissante
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ← EXACTEMENT CE QUE LE CHECK VEUT
        Like.objects.get_or_create(user=request.user, post=post)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )

        return Response({'status': 'liked'})


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ← EXACTEMENT CE QUE LE CHECK VEUT
        Like.objects.filter(user=request.user, post=post).delete()

        return Response({'status': 'unliked'})