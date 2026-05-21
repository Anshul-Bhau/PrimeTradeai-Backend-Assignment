from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, UserSerializer

# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/

    Public endpoint. Accepts username, email, password, password2,
    and optional role. Creates a new user and returns 201 on success.
    Returns 400 with field-level errors if validation fails.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """
    POST /api/v1/auth/login/

    Public endpoint. Accepts email and password.
    On success returns a JWT access token, refresh token, and
    basic user data. Returns 401 on invalid credentials.
    """
    permission_classes= [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required.'}, status=400)

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
            'user':    UserSerializer(user).data,
        })
    

class MeView(APIView):
    """
    GET /api/v1/auth/me/

    Protected endpoint. Requires a valid JWT Bearer token.
    Returns the currently authenticated user's profile data.
    Used by the frontend to verify the session and display user info.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)
    
    