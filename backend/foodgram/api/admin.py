from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
