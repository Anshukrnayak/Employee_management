from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app.models import LeadModel, ClientModel
from .serializers import LeadSerializer, ClientSerializer

class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeadSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        """Return only leads belonging to the current user with optimized queries."""
        return (
            LeadModel.objects
            .filter(user=self.request.user)
            .prefetch_related('clients')
            .select_related('user')
        )

    def perform_create(self, serializer):
        """Automatically assign the lead to the current user with validation."""
        if LeadModel.objects.filter(user=self.request.user).exists():
            raise ValidationError(
                {"detail": "User can only have one lead profile."},
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)

    def get_object(self):
        """Ensure users can only access their own leads with proper 404 handling."""
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        """Custom delete handler to prevent accidental lead deletion."""
        instance = self.get_object()
        if instance.clients.exists():
            return Response(
                {"detail": "Cannot delete lead with associated clients."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        """Return only clients linked to the current user's lead with optimized queries."""
        return (
            ClientModel.objects
            .filter(lead__user=self.request.user)
            .select_related('lead', 'lead__user')
        )

    def perform_create(self, serializer):
        """Automatically assign the client to the current user's lead with validation."""
        lead = get_object_or_404(
            LeadModel.objects.filter(user=self.request.user),
            msg="No lead profile found for this user."
        )
        serializer.save(lead=lead)

    def get_object(self):
        """Ensure users can only access their own clients with proper 404 handling."""
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        """Add custom update logic if needed."""
        super().perform_update(serializer)
        # Additional update logic can be added here