from rest_framework import serializers

from .models import Character


class CharacterSerializer(serializers.ModelSerializer):
    """Convertit un personnage entre modèle Django et données JSON."""

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Character
        fields = (
            "id",
            "owner",
            "name",
            "level",
            "experience",
            "description",
            "strength",
            "agility",
            "endurance",
            "intelligence",
            "perception",
            "willpower",
            "charisma",
            "current_health",
            "current_stamina",
            "current_mana",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")
        extra_kwargs = {
            "level": {"min_value": 1},
            "experience": {"min_value": 0},
            "strength": {"min_value": 1},
            "agility": {"min_value": 1},
            "endurance": {"min_value": 1},
            "intelligence": {"min_value": 1},
            "perception": {"min_value": 1},
            "willpower": {"min_value": 1},
            "charisma": {"min_value": 1},
            "current_health": {"min_value": 0},
            "current_stamina": {"min_value": 0},
            "current_mana": {"min_value": 0},
        }

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 2 caractères."
            )

        owner = self.context["request"].user
        characters = Character.objects.filter(owner=owner, name__iexact=value)

        if self.instance is not None:
            characters = characters.exclude(pk=self.instance.pk)

        if characters.exists():
            raise serializers.ValidationError(
                "Vous possédez déjà un personnage portant ce nom."
            )
        return value

    def validate_description(self, value):
        value = value.strip()
        if len(value) > 2000:
            raise serializers.ValidationError(
                "La description ne peut pas dépasser 2000 caractères."
            )
        return value
