import csv
from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import OwnerOrReadOnly
from .serializers import (FavoritesSerializer, IngredientSerializer,
                          PurchaseSerializer, RecipeListSerializer,
                          RecipePostSerializer, SubscriptionSerializer,
                          TagSerializer)

from recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                            RecipeIngredient, Subscription, Tag)
from users.models import User


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipePostSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, RecipeFilter)
    filterset_fileds = ('tags__slug',)
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipePostSerializer

    def _add_favorite_or_purchase(self, request, pk, input_serializer):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'recipe': recipe.id,
        }
        serializer = input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(HTTPStatus.CREATED)

    def _del_favorite_or_purchase(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        instance = get_object_or_404(model, user=user, recipe=recipe)
        instance.delete()

    @action(detail=True, methods=['post', ])
    def favorite(self, request, pk):
        return self._add_favorite_or_purchase(request, pk, FavoritesSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        self._del_favorite_or_purchase(request, pk, Favorite)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', ])
    def shopping_cart(self, request, pk):
        return self._add_favorite_or_purchase(request, pk, PurchaseSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        self._del_favorite_or_purchase(request, pk, Purchase)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get', ])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__purchase__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount')
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'ingredient_amount'
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="shoppinglist.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for row in list(ingredients):
            writer.writerow(row)
        return response


class SubscriptionList(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('users_id')
        subscribed_to = get_object_or_404(User, id=user_id)
        Subscription.objects.get_or_create(
            user=user,
            subscribed_to=subscribed_to
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('users_id')
        subscribed_to = get_object_or_404(User, id=user_id)
        Subscription.objects.filter(
            user=user,
            subscribed_to=subscribed_to
        ).delete()
        return Response(HTTPStatus.NO_CONTENT)


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, OrderingFilter)
    permission_classes = (AllowAny,)
    pagination_class = None
    search_fields = ('^name',)
    ordering_fields = ('id',)
