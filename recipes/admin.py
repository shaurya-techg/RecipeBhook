from django.contrib import admin

from .models import GeneratedRecipe


@admin.register(GeneratedRecipe)
class GeneratedRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "generation_mode",
        "difficulty",
        "is_favorite",
        "created_at",
    )

    list_filter = (
        "generation_mode",
        "difficulty",
        "is_favorite",
    )

    search_fields = (
        "title",
        "user__username",
    )

    readonly_fields = ("created_at",)