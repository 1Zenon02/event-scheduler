from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Write-only field for password input.
    password = serializers.CharField(write_only=True)
    # Read-only field for returning the token.
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token')

    def create(self, validated_data):
        # Use create_user to ensure password is hashed.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        # Create a token for the new user.
        token, created = Token.objects.get_or_create(user=user)
        # Attach token key to serializer output.
        user.token = token.key
        return user
