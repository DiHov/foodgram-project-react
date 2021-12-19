from .models import IngredientAmount


def ingredient_creaton(recipe, ingredients):
    amounts_instance = []
    for ingredient_data in ingredients:
        amount = ingredient_data['amount']
        ingredient = ingredient_data['id']
        amounts_instance.append(
            IngredientAmount(
                amount=amount,
                recipe=recipe,
                ingredient=ingredient
            )
        )
    return IngredientAmount.objects.bulk_create(amounts_instance)
