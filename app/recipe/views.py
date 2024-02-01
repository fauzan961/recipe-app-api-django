"""
Views for the recipe API.
"""
from rest_framework import (viewsets, mixins)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Recipe, Tag)
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
        
        return self.serializer_class
    
    def perform_create(self, serializer): # Perform_create method executes just before saving the creation of new record in db.
        """Add user to the existing recipe field"""
        serializer.save(user=self.request.user) # Adding value to the user field and pass the user field for creating new record.

class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for managing tag APIS."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retrieve tags filtered on authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
