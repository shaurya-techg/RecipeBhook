from django.urls import path

from . import views


app_name = "recipes"


urlpatterns = [
    path(
        "ingredients/",
        views.ingredient_recipe,
        name="ingredient_recipe",
    ),

    path(
        "guide/",
        views.guide_recipe,
        name="guide_recipe",
    ),

    path(
        "my-recipes/",
        views.my_recipes,
        name="my_recipes",
    ),

    path(
        "favorites/",
        views.favorites,
        name="favorites",
    ),

    path(
        "<int:recipe_id>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),

    path(
        "<int:recipe_id>/generate-audio/",
        views.generate_recipe_audio_view,
        name="generate_recipe_audio",
    ),
    
    path(
        "<int:recipe_id>/generate-hindi-audio/",
        views.generate_hindi_recipe_audio_view,
        name="generate_hindi_recipe_audio"
    ),

    path(
        "<int:recipe_id>/",
        views.recipe_detail,
        name="recipe_detail",
    ),
]