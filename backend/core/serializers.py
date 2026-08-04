from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Expose uniquement les informations publiques du compte."""

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Valide les données et crée un nouvel utilisateur."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "password_confirm")
        read_only_fields = ("id",)

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
