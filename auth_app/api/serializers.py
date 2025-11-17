from rest_framework import serializers

from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        pw = self.validated_data['password']
        rp = self.validated_data['repeated_password']

        if pw != rp:
            raise serializers.ValidationError(
                {"password": "Passwords must match."})

        fullname = self.validated_data['fullname'].strip()
        parts = fullname.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        account.set_password(pw)
        account.save()
        return account

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "email already exists.")
        return value

    def validate_fullname(self, value):
        value = value.strip()
        parts = value.split()

        if len(parts) < 2:
            raise serializers.ValidationError(
                "Please enter both first and last name.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid email or password.")

        data['user'] = user
        return data


class UserPreviewSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
