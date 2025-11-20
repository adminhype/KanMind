from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from .serializers import RegistrationSerializer, LoginSerializer, UserPreviewSerializer


def get_auth_response(user):
    """
    helper to create the response dict
    """
    token, created = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'fullname': f"{user.first_name} {user.last_name}".strip(),
        'email': user.email,
        'user_id': user.id
    }


class RegistrationView(APIView):
    """
    API View for user registration.
    allows any user to create a new account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            data = get_auth_response(saved_account)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    """
    API View for user login.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles the POST request for user login.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            data = get_auth_response(user)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """
    API view to check if an email address exists in DB.
    only accessible to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        handles the GET request.
        email: Email address to check.
        """
        email = request.query_params.get('email')

        if not email or not self.is_valid_email(email):
            return Response({"error": "Invalid or missing email."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserPreviewSerializer(user).data)

    def is_valid_email(self, email):
        """
        validates the given email address.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
