from django import forms


class IngredientRecipeForm(forms.Form):

    ingredients = forms.CharField(
        label="Available Ingredients",
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": (
                    "Example: potatoes, onions, tomatoes, eggs"
                ),
                "class": (
                    "w-full resize-none rounded-xl border-0 bg-transparent "
                    "px-5 py-4 text-stone-800 outline-none "
                    "placeholder:text-stone-400 focus:outline-none "
                    "focus:ring-0"
                ),
            }
        ),
    )


class GuideRecipeForm(forms.Form):

    request = forms.CharField(
        label="What would you like to cook?",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": (
                    "Example: How do I make paneer butter masala?"
                ),
                "class": (
                    "w-full resize-none rounded-xl border-0 bg-transparent "
                    "px-5 py-4 text-stone-800 outline-none "
                    "placeholder:text-stone-400 focus:outline-none "
                    "focus:ring-0"
                ),
            }
        ),
    )