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

    def validate_name(self, value):
        owner = self.context["request"].user
        characters = Character.objects.filter(owner=owner, name=value)

        if self.instance is not None:
            characters = characters.exclude(pk=self.instance.pk)

        if characters.exists():
            raise serializers.ValidationError(
                "Vous possédez déjà un personnage portant ce nom."
            )
        return value
