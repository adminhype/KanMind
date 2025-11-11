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
