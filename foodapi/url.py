from django.urls import path
from foodapi.views import TagView, IngredientView, RecipeView, AllRecipeView

urlpatterns = [
    path('tag/', TagView.as_view()),
    path('ingredients/', IngredientView.as_view()),
    path('recipe/', RecipeView.as_view()),
    path('allRecipe/', AllRecipeView.as_view()),
]
