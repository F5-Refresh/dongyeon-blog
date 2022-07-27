from rest_framework.response import Response
from rest_framework import status
from post.models import HashTag, Post
from post.serializer import DetailSerializer, GetSerializer, PatchSerializer, PostSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

PagePer = 10

class PostView(APIView):

	def get(self, req):
		page = int(req.GET.get('page', 0))
		posts = Post.active()[page * PagePer: (page+1) * PagePer]

		serializer = GetSerializer(data=posts, many=True)
		serializer.is_valid()
		return Response(serializer.data,status=status.HTTP_200_OK)

	def post(self, req):
		serializer = PostSerializer(data=req.data | {'user': req.user.id }, context={'hash_tags': req.data.get('hash_tags', '')})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, req, id):
		post = get_object_or_404(Post, user=req.user, id=id)
		serializer = PatchSerializer(data=req.data, instance=post)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	# soft delete만들어야함
	def delete(self, req, id):
		post = get_object_or_404(Post, user=req.user, id=id)
		post.delete = not post.delete
		post.save()
		return Response(status=status.HTTP_200_OK)
	
	@api_view(['GET'])
	def detail(req, id):
		post = get_object_or_404(Post, id=id, delete_flag=False)
		post.views += 1
		post.save()
		serializer = DetailSerializer(post)
		return Response(serializer.data, status=status.HTTP_200_OK)
		
	@api_view(['POST'])
	def like(req, id):
		user = req.user
		post = get_object_or_404(Post, id=id, delete_falg=False)
		if post.likes.filter(id=user.id):
			user.like_posts.remove(post)
			return Response({'message': '좋아요가 삭제되었습니다.'},status=status.HTTP_200_OK)
		else:
			user.like_posts.add(post)
			user.save()
			return Response({'message': '좋아요가 등록되었습니다.'},status=status.HTTP_200_OK)

	@api_view(['GET'])
	def search(req):
		page = int(req.GET.get('page', 0))
		posts = Post.active().filter(hash_tags__name=req.GET.get('hash_tag', ''))[page * PagePer: (page+1) * PagePer]
		serializer = GetSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)