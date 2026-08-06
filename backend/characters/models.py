from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q, Value
from django.db.models.functions import Length, Lower, Trim
from django.db.models.lookups import GreaterThanOrEqual, LessThanOrEqual


class Character(models.Model):
    """Personnage de jeu appartenant à un utilisateur."""

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        ACTIVE = "active", "Actif"
        INACTIVE = "inactive", "Inactif"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters",
        verbose_name="propriétaire",
    )
    name = models.CharField("nom", max_length=100)
    level = models.PositiveIntegerField(
        "niveau",
        default=1,
        validators=[MinValueValidator(1)],
    )
    experience = models.PositiveIntegerField("expérience", default=0)
    description = models.TextField("description", blank=True)
    strength = models.PositiveSmallIntegerField(
        "force",
        default=1,
        validators=[MinValueValidator(1)],
    )
    agility = models.PositiveSmallIntegerField(
        "agilité",
        default=1,
        validators=[MinValueValidator(1)],
    )
    endurance = models.PositiveSmallIntegerField(
        "endurance",
        default=1,
        validators=[MinValueValidator(1)],
    )
    intelligence = models.PositiveSmallIntegerField(
        "intelligence",
        default=1,
        validators=[MinValueValidator(1)],
    )
    perception = models.PositiveSmallIntegerField(
        "perception",
        default=1,
        validators=[MinValueValidator(1)],
    )
    willpower = models.PositiveSmallIntegerField(
        "volonté",
        default=1,
        validators=[MinValueValidator(1)],
    )
    charisma = models.PositiveSmallIntegerField(
        "charisme",
        default=1,
        validators=[MinValueValidator(1)],
    )
    current_health = models.PositiveIntegerField("PV actuels", default=0)
    current_stamina = models.PositiveIntegerField("endurance actuelle", default=0)
    current_mana = models.PositiveIntegerField("mana actuel", default=0)
    status = models.CharField(
        "statut",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField("créé le", auto_now_add=True)
    updated_at = models.DateTimeField("modifié le", auto_now=True)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                F("owner"),
                Lower(Trim("name")),
                name="unique_character_name_ci_per_owner",
            ),
            models.CheckConstraint(
                condition=GreaterThanOrEqual(Length(Trim(F("name"))), Value(2)),
                name="character_name_min_2_chars",
            ),
            models.CheckConstraint(
                condition=LessThanOrEqual(Length(F("description")), Value(2000)),
                name="character_description_max_2000_chars",
            ),
            models.CheckConstraint(
                condition=Q(level__gte=1),
                name="character_level_gte_1",
            ),
            models.CheckConstraint(
                condition=(
                    Q(strength__gte=1)
                    & Q(agility__gte=1)
                    & Q(endurance__gte=1)
                    & Q(intelligence__gte=1)
                    & Q(perception__gte=1)
                    & Q(willpower__gte=1)
                    & Q(charisma__gte=1)
                ),
                name="character_stats_gte_1",
            ),
            models.CheckConstraint(
                condition=Q(experience__gte=0)
                & Q(current_health__gte=0)
                & Q(current_stamina__gte=0)
                & Q(current_mana__gte=0),
                name="character_resources_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(status__in=("pending", "active", "inactive")),
                name="character_status_valid",
            ),
        ]
        verbose_name = "personnage"
        verbose_name_plural = "personnages"

    def __str__(self):
        return self.name
