import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


GROQ_MODEL = "openai/gpt-oss-20b"


def get_groq_client():
    """
    Create and return a Groq client using the API key
    stored in the environment.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. "
            "Check your .env file."
        )

    return Groq(api_key=api_key)


def generate_recipe_from_ingredients(ingredients):
    """
    Generate a structured recipe using the ingredients
    provided by the user.
    """

    client = get_groq_client()

    prompt = f"""
You are RecipeBhook, an expert cooking assistant.

Create a practical and delicious recipe using the ingredients provided
by the user.

User's available ingredients:
{ingredients}

You may assume the user has basic kitchen essentials such as:
salt, water, and cooking oil.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "Recipe name",
    "ingredients": [
        "ingredient with quantity",
        "ingredient with quantity"
    ],
    "instructions": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    "prep_time": 10,
    "cook_time": 20,
    "total_time": 30,
    "servings": 2,
    "difficulty": "easy",
    "tips": [
        "Helpful cooking tip"
    ]
}}

Rules:
- prep_time, cook_time, total_time, and servings must be numbers.
- difficulty must be exactly one of: easy, medium, hard.
- total_time should equal prep_time + cook_time.
- Return JSON only.
- Do not use markdown code blocks.
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7,
        max_completion_tokens=1500,
    )

    response_text = completion.choices[0].message.content

    recipe_data = json.loads(response_text)

    return recipe_data


def generate_recipe_from_request(user_request):
    """
    Generate a structured recipe based on a dish or
    cooking request provided by the user.
    """

    client = get_groq_client()

    prompt = f"""
You are RecipeBhook, an expert cooking assistant.

The user wants cooking guidance for the following request:

{user_request}

Analyze the request and provide a practical, clear, and complete
recipe or cooking solution.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "Recipe name",
    "ingredients": [
        "ingredient with quantity",
        "ingredient with quantity"
    ],
    "instructions": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    "prep_time": 10,
    "cook_time": 20,
    "total_time": 30,
    "servings": 2,
    "difficulty": "easy",
    "tips": [
        "Helpful cooking tip"
    ]
}}

Rules:
- Understand the user's request and generate the most relevant recipe.
- Give clear, beginner-friendly instructions.
- prep_time, cook_time, total_time, and servings must be numbers.
- difficulty must be exactly one of: easy, medium, hard.
- total_time should equal prep_time + cook_time.
- Return JSON only.
- Do not use markdown code blocks.
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7,
        max_completion_tokens=1500,
    )

    response_text = completion.choices[0].message.content

    recipe_data = json.loads(response_text)

    return recipe_data


def translate_recipe_to_hindi(recipe):
    """
    Translate a recipe into Hindi for Amazon Polly audio generation.

    Returns plain Hindi text only.
    """

    client = get_groq_client()

    ingredients_text = "\n".join(
        f"- {ingredient}"
        for ingredient in recipe.ingredients
    )

    instructions_text = "\n".join(
        f"{index}. {instruction}"
        for index, instruction in enumerate(
            recipe.instructions,
            start=1,
        )
    )

    tips_text = ""

    if recipe.tips:
        tips_text = "\n".join(
            f"- {tip}"
            for tip in recipe.tips
        )

    prompt = f"""
You are a professional recipe translator.

Translate the following recipe from English into natural,
easy-to-understand Hindi (Devanagari script).

This translation will be spoken aloud to a user while cooking.

Rules:
- Return ONLY the Hindi translation.
- Do not use Markdown.
- Do not add explanations.
- Keep ingredient quantities accurate.
- Make the instructions clear and natural when spoken aloud.
- Use Hindi (Devanagari script), not Roman Hindi.
- Keep cooking terms understandable for an Indian audience.

Recipe title:
{recipe.title}

Ingredients:
{ingredients_text}

Instructions:
{instructions_text}

Prep time: {recipe.prep_time} minutes
Cook time: {recipe.cook_time} minutes
Total time: {recipe.total_time} minutes
Servings: {recipe.servings}

Tips:
{tips_text}
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
        max_completion_tokens=2000,
    )

    return completion.choices[0].message.content.strip()