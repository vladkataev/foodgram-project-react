from django.contrib import admin
from django.db.models import Count

from .models import (Favorite, Ingredient, Purchase,
                     Recipe, RecipeIngredient, Subscription,
                     Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_favorited',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('is_favorited',)

    def is_favorited(self, obj):
        result = Recipe.objects.filter(
            id=obj.id
        ).aggregate(Count('is_favorited'))
        return result['is_favorited__count']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscription)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(Purchase)
