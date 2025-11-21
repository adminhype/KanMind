from rest_framework import serializers

from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for user registration.
    """
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """
        check if passwords match.
        """
        if attrs.get('password') != attrs.get('repeated_password'):
            raise serializers.ValidationError(
                {"password": "Passwords must match."})
        return attrs

    def save(self):
        """
        saves the new user and split fullname
        """
        fullname = self.validated_data['fullname'].strip()
        first_name, *last_parts = fullname.split(' ', 1)
        last_name = last_parts[0] if last_parts else ''

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        account.set_password(self.validated_data['password'])
        account.save()
        return account

    def validate_email(self, value):
        """
        checks if the email is already registered
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "email already exists.")
        return value

    def validate_fullname(self, value):
        """
        checks if the fullname contains at least two words.
        """
        value = value.strip()
        parts = value.split()

        if len(parts) < 2:
            raise serializers.ValidationError(
                "Please enter both first and last name.")
        return value


class LoginSerializer(serializers.Serializer):
    """
    serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        checks if the user exsist (case-insensitive) and password is correct.
        """
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."})
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"password": "Incorrect password."})

        data['user'] = user
        return data


class UserPreviewSerializer(serializers.ModelSerializer):
    """
    serializer to display basic user information."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
