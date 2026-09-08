import os

import boto3

from services.ai.groq_service import translate_recipe_to_hindi


AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")


def get_polly_client():
    """
    Create and return an Amazon Polly client.
    """

    return boto3.client(
        "polly",
        region_name=AWS_REGION,
    )


def generate_recipe_audio(recipe):
    """
    Generate an English MP3 narration for a recipe.

    Returns the audio bytes.
    """

    polly = get_polly_client()

    narration_parts = [
        f"Welcome to RecipeBhook. Today we are making {recipe.title}.",
        f"This recipe serves {recipe.servings} people.",
        f"The preparation time is {recipe.prep_time} minutes.",
        f"The cooking time is {recipe.cook_time} minutes.",
        "Let's start with the ingredients.",
    ]

    for ingredient in recipe.ingredients:
        narration_parts.append(ingredient)

    narration_parts.append(
        "Now, let's move on to the cooking instructions."
    )

    for index, instruction in enumerate(
        recipe.instructions,
        start=1,
    ):
        narration_parts.append(
            f"Step {index}. {instruction}"
        )

    if recipe.tips:
        narration_parts.append(
            "Here are some helpful cooking tips."
        )

        for tip in recipe.tips:
            narration_parts.append(tip)

    narration_parts.append(
        "Your recipe is now complete. Happy cooking!"
    )

    narration = " ".join(narration_parts)

    response = polly.synthesize_speech(
        Text=narration,
        OutputFormat="mp3",
        VoiceId="Aditi",
        Engine="standard",
    )

    return response["AudioStream"].read()


def generate_hindi_recipe_audio(recipe):
    """
    Translate the recipe into Hindi using Groq
    and generate Hindi MP3 narration using
    Amazon Polly's Aditi voice.

    Returns the audio bytes.
    """

    hindi_narration = translate_recipe_to_hindi(recipe)

    polly = get_polly_client()

    response = polly.synthesize_speech(
        Text=hindi_narration,
        OutputFormat="mp3",
        VoiceId="Aditi",
        Engine="standard",
        LanguageCode="hi-IN",
    )

    return response["AudioStream"].read()