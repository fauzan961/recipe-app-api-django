"""
Views for the recipe API.
"""
from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Recipe, Tag, Ingredient)
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIS."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # Overriding the queryset set above to filter the records based on the logged in user.
    def get_queryset(self):
        """Retrieve recipes filtered on authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    # Overriding the serializer_class set above to switch serializer for detail view.
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer): # Perform_create method executes just before saving the creation of new record in db.
        """Add user to the existing recipe field"""
        serializer.save(user=self.request.user) # Adding value to the user field and pass the user field for creating new record.
        
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload Image to recipe API."""
        recipe = self.get_object() # Retrieve the recipe object based on the id of the recipe.
        serializer = self.get_serializer(recipe, data=request.data) # Runs get_serializer_class and gets the serializer as declared above.
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base Viewset for Tags and Ingredients."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retrieve tags filtered on authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
class TagViewSet(BaseRecipeAttrViewSet):
    """View for managing tag APIS."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    """View for managing Ingredients APIs."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    