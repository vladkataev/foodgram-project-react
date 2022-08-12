from django.contrib import admin
from django.db.models import Count
from .models import (Favorite, Ingredient, Purchase,
                     Recipe, RecipeIngredient, Subscription,
                     Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',
                    'cooking_time', 'pub_date',
                    'is_favorited',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('is_favorited',)

    def is_favorited(self, obj):
        result = Recipe.objects.filter(
            id=obj.id
        ).aggregate(Count('is_favorited'))
        return result['is_favorited__count']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed_to')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
