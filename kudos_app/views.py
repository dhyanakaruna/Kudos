from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Organization, User, Kudo
from .serializers import (
    OrganizationSerializer, UserSerializer, UserSimpleSerializer, 
    KudoSerializer, KudoCreateSerializer
)


class SimpleAuthenticationMixin:
    """Simple authentication mixin that gets user ID from headers"""
    
    def dispatch(self, request, *args, **kwargs):
        # Get user ID from X-User-ID header (simple authentication)
        user_id = request.headers.get('X-User-ID')
        if user_id:
            try:
                request.user_id = int(user_id)
                request.current_user = User.objects.get(id=user_id)
            except (ValueError, User.DoesNotExist):
                request.user_id = None
                request.current_user = None
        else:
            request.user_id = None
            request.current_user = None
        
        return super().dispatch(request, *args, **kwargs)


@api_view(['GET'])
def current_user(request):
    """Get current user information including remaining kudos"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return Response({'error': 'X-User-ID header required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=int(user_id))
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except (ValueError, User.DoesNotExist):
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)


class UserListView(SimpleAuthenticationMixin, generics.ListAPIView):
    """List all users in the same organization as the current user"""
    serializer_class = UserSimpleSerializer
    
    def get_queryset(self):
        if not self.request.current_user:
            return User.objects.none()
        
        # Return users in the same organization, excluding the current user
        return User.objects.filter(
            organization=self.request.current_user.organization
        ).exclude(id=self.request.current_user.id).order_by('username')


class KudoCreateView(SimpleAuthenticationMixin, generics.CreateAPIView):
    """Create a new kudo"""
    serializer_class = KudoCreateSerializer
    
    def perform_create(self, serializer):
        if not self.request.current_user:
            raise ValueError("Authentication required")
        
        serializer.save(sender=self.request.current_user)
    
    def create(self, request, *args, **kwargs):
        if not request.current_user:
            return Response(
                {'error': 'X-User-ID header required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)


class KudosReceivedView(SimpleAuthenticationMixin, generics.ListAPIView):
    """List all kudos received by the current user"""
    serializer_class = KudoSerializer
    
    def get_queryset(self):
        if not self.request.current_user:
            return Kudo.objects.none()
        
        return Kudo.objects.filter(receiver=self.request.current_user).select_related('sender')


@api_view(['GET'])
def organizations_list(request):
    organizations = Organization.objects.all()
    serializer = OrganizationSerializer(organizations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def users_by_organization(request, org_id):
    try:
        organization = Organization.objects.get(id=org_id)
        users = User.objects.filter(organization=organization).order_by('username')
        serializer = UserSimpleSerializer(users, many=True)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
