from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts username, email, password, password2, and optional role.
    Validates that both passwords match, hashes the password, and
    creates the user. password and password2 are write-only and
    never returned in responses.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')
        extra_kwargs = {'role' : {'default' : 'user', 'required' : False},
                        'password':{'write_only' : True}
                        }

    def validate(self, attrs):
        """
        Ensure password and password2 match before proceeding.
        Raises ValidationError if they differ.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password' :'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        """
        Remove password2 from data, hash the password using set_password(),
        and persist the new User instance to the database.
        """
        validated_data.pop('password2')
        self.password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(self.password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Read-only serializer
    Exposes id, username, email, and role. Never exposes password.
    Used in login responses and the /me/ endpoint.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')
