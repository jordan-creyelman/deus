from django.contrib import admin

from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "level",
        "current_health",
        "current_stamina",
        "current_mana",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("name", "owner__username")
