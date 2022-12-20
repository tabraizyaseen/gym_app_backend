from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes

from .models import User
from .serializer import NewUserSerializer, ReturningUserSerializer

# Create your views here.
@permission_classes([AllowAny])
class registerAthlete(APIView):
    " Registering new users and serving returning users "
    def post(self, request):
        try:
            # Serving Returning Users
            check_user = User.objects.get(email=request.data.get('email'), password=request.data.get('password'))
            serializer_obj = ReturningUserSerializer(data=request.data)
            if serializer_obj.is_valid():
                token, _ = Token.objects.get_or_create(user_id=check_user.id)
                return Response({
                    'error': False, 
                    'message':'user already existed', 
                    'data':[{'auth_token': token.key}]},
                    status=status.HTTP_200_OK)
            return Response({
                    'error': True, 
                    'message':'Entered Data is Incorrect', 
                    'data':[serializer_obj.errors]},
                    status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            # Serving New Users
            serializer_obj = NewUserSerializer(data=request.data)
            if serializer_obj.is_valid():
                user_obj = serializer_obj.save()
                token, _ = Token.objects.get_or_create(user_id=user_obj.id)
                return Response({
                    'error': False, 
                    'message':'new user registered', 
                    'data':[{'auth_token': token.key}]},
                    status=status.HTTP_201_CREATED)
            return Response({
                    'error': True, 
                    'message':'Entered Data is Incorrect', 
                    'data':[serializer_obj.errors]},
                    status=status.HTTP_400_BAD_REQUEST)