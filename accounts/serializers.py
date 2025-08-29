from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {
            "email": {
                "error_messages": {
                    'unique': "An account with this email already exists."
                }
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data.get("name", "")
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for returning user info."""
    class Meta:
        model = User
        fields = fields = ["id", "email", "name", "date_joined"]
