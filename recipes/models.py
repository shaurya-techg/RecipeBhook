from django.conf import settings
from django.db import models


class GeneratedRecipe(models.Model):
    GENERATION_MODE_CHOICES = [
        ("ingredients", "What Can I Cook?"),
        ("guide", "Guide Me to Cook"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_recipes",
    )

    title = models.CharField(max_length=255)

    generation_mode = models.CharField(
        max_length=20,
        choices=GENERATION_MODE_CHOICES,
    )

    original_request = models.TextField()

    ingredients = models.JSONField()

    instructions = models.JSONField()

    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes"
    )

    cook_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )

    total_time = models.PositiveIntegerField(
        help_text="Total time in minutes"
    )

    servings = models.PositiveIntegerField()

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
    )

    tips = models.JSONField(
        default=list,
        blank=True,
    )

    is_favorite = models.BooleanField(default=False)

    # English audio
    audio_file = models.FileField(
     upload_to="recipe_audio/",
     blank=True,
     null=True,
    )

    # Cached Hindi translation
    hindi_translation = models.TextField(
        blank=True,
        null=True,
    )

    # Hindi audio
    hindi_audio_file = models.FileField(
        upload_to="recipe_audio/hindi/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user}"