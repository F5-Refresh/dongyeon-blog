from rest_framework.response import Response
from rest_framework import status
from user.serializer import UserSignInSerializer, UserSignUpSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# Create your views here.


class UserView(APIView):
	@api_view(['POST'])
	def sign_up(req):
		user = UserSignUpSerializer(data=req.data)
		if user.is_valid():
			user.save()
			return Response(user.data)
		return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@api_view(['POST'])
	def sign_in(req):
		user = UserSignInSerializer(data=req.data)
		if user.is_valid:
			return Response(user.user_signin(req.data))
		return Response(user.errors) 