from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)
from django.shortcuts import render, get_object_or_404, redirect
from .forms import IngredientRecipeForm, GuideRecipeForm
from .models import GeneratedRecipe
from django.core.files.base import ContentFile

from services.audio.polly_service import (
    generate_recipe_audio,
    generate_hindi_recipe_audio,
)
from services.ai.groq_service import (
    generate_recipe_from_ingredients,
    generate_recipe_from_request,
)

RECIPE_DETAIL_URL = "recipes:recipe_detail"

@login_required
@require_http_methods(["GET", "POST"])
def ingredient_recipe(request):
    error_message = None

    if request.method == "POST":
        form = IngredientRecipeForm(request.POST)

        if form.is_valid():
            submitted_ingredients = form.cleaned_data["ingredients"]

            try:
                recipe_data = generate_recipe_from_ingredients(
                    submitted_ingredients
                )

                recipe = GeneratedRecipe.objects.create(
                    user=request.user,
                    title=recipe_data["title"],
                    generation_mode="ingredients",
                    original_request=submitted_ingredients,
                    ingredients=recipe_data["ingredients"],
                    instructions=recipe_data["instructions"],
                    prep_time=recipe_data["prep_time"],
                    cook_time=recipe_data["cook_time"],
                    total_time=recipe_data["total_time"],
                    servings=recipe_data["servings"],
                    difficulty=recipe_data["difficulty"],
                    tips=recipe_data.get("tips", []),
                )

                # Redirect after successful POST
                return redirect(
                    RECIPE_DETAIL_URL,
                    recipe_id=recipe.id,
                )

            except Exception as error:
                error_message = (
                    "We couldn't generate your recipe right now. "
                    "Please try again."
                )

                print(
                    f"Groq recipe generation error: {error}"
                )

    else:
        form = IngredientRecipeForm()

    return render(
        request,
        "recipes/ingredient_recipe.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def guide_recipe(request):
    submitted_request = None
    recipe = None
    error_message = None

    if request.method == "POST":
        form = GuideRecipeForm(request.POST)

        if form.is_valid():
            submitted_request = form.cleaned_data["request"]

            try:
                recipe_data = generate_recipe_from_request(
                    submitted_request
                )

                recipe = GeneratedRecipe.objects.create(
                    user=request.user,
                    title=recipe_data["title"],
                    generation_mode="guide",
                    original_request=submitted_request,
                    ingredients=recipe_data["ingredients"],
                    instructions=recipe_data["instructions"],
                    prep_time=recipe_data["prep_time"],
                    cook_time=recipe_data["cook_time"],
                    total_time=recipe_data["total_time"],
                    servings=recipe_data["servings"],
                    difficulty=recipe_data["difficulty"],
                    tips=recipe_data.get("tips", []),
                )

            except Exception as error:
                error_message = (
                    "We couldn't generate cooking guidance right now. "
                    "Please try again."
                )

                print(
                    f"Groq guide recipe generation error: {error}"
                )

    else:
        form = GuideRecipeForm()

    return render(
        request,
        "recipes/guide_recipe.html",
        {
            "form": form,
            "submitted_request": submitted_request,
            "recipe": recipe,
            "error_message": error_message,
        },
    )
    
@login_required
@require_POST
def generate_recipe_audio_view(request, recipe_id):
    recipe = get_object_or_404(
        GeneratedRecipe,
        id=recipe_id,
        user=request.user,
    )

    # Reuse existing audio and avoid another Polly API call
    if not recipe.audio_file:
        try:
            audio_bytes = generate_recipe_audio(recipe)

            filename = f"recipe_{recipe.id}.mp3"

            recipe.audio_file.save(
                filename,
                ContentFile(audio_bytes),
                save=True,
            )

        except Exception as error:
            print(f"Amazon Polly audio generation error: {error}")

    return redirect(
        RECIPE_DETAIL_URL,
        recipe_id=recipe.id,
    )

@login_required
@require_POST
def generate_hindi_recipe_audio_view(request, recipe_id):
    recipe = get_object_or_404(
        GeneratedRecipe,
        id=recipe_id,
        user=request.user,
    )

    # Reuse existing Hindi audio
    if not recipe.hindi_audio_file:
        try:
            audio_bytes = generate_hindi_recipe_audio(recipe)

            filename = f"recipe_{recipe.id}_hindi.mp3"

            recipe.hindi_audio_file.save(
                filename,
                ContentFile(audio_bytes),
                save=True,
            )

        except Exception as error:
            print(
                f"Amazon Polly Hindi audio generation error: {error}"
            )

    return redirect(
        RECIPE_DETAIL_URL,
        recipe_id=recipe.id,
    )
    
@login_required
@require_GET
def my_recipes(request):
    recipes = GeneratedRecipe.objects.filter(user=request.user)

    return render(
        request,
        "recipes/my_recipes.html",
        {"recipes": recipes},
    )


@login_required
@require_GET
def favorites(request):
    recipes = GeneratedRecipe.objects.filter(
        user=request.user,
        is_favorite=True,
    )

    return render(
        request,
        "recipes/favorites.html",
        {"recipes": recipes},
    )

@login_required
@require_GET
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(
        GeneratedRecipe,
        id=recipe_id,
        user=request.user,
    )

    return render(
        request,
        "recipes/recipe_detail.html",
        {"recipe": recipe},
    )

@login_required
@require_POST
def toggle_favorite(request, recipe_id):

    recipe = get_object_or_404(
        GeneratedRecipe,
        id=recipe_id,
        user=request.user,
    )

    recipe.is_favorite = not recipe.is_favorite
    recipe.save()

    return redirect(
        RECIPE_DETAIL_URL,
        recipe_id=recipe.id,
    )