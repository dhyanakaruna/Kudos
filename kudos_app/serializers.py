from rest_framework import serializers
from .models import Organization, User, Kudo
from datetime import datetime, timedelta


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    remaining_kudos = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'organization', 'organization_name', 'remaining_kudos', 'created_at']
    
    def get_remaining_kudos(self, obj):
        return obj.get_remaining_kudos()


class UserSimpleSerializer(serializers.ModelSerializer):
    """Simplified user serializer for dropdowns and references"""
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'organization_name']


class KudoSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    
    class Meta:
        model = Kudo
        fields = ['id', 'sender', 'receiver', 'sender_username', 'receiver_username', 'message', 'created_at']
        read_only_fields = ['sender']  # Sender will be set from the authenticated user
    
    def validate(self, data):
        """Custom validation for kudos"""
        request = self.context.get('request')
        if request and hasattr(request, 'user_id'):
            sender_id = request.user_id
            receiver_id = data.get('receiver').id
            
            # Check if trying to send to self
            if sender_id == receiver_id:
                raise serializers.ValidationError("You cannot give kudos to yourself.")
            
            # Check if sender has remaining kudos
            try:
                sender = User.objects.get(id=sender_id)
                if sender.get_remaining_kudos() <= 0:
                    raise serializers.ValidationError("You have no remaining kudos for this week.")
                
                # Check if sender and receiver are in the same organization
                receiver = data.get('receiver')
                if sender.organization != receiver.organization:
                    raise serializers.ValidationError("You can only give kudos to users in your organization.")
                    
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid sender.")
        
        return data


class KudoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating kudos"""
    class Meta:
        model = Kudo
        fields = ['receiver', 'message']
    
    def validate(self, data):
        """Custom validation for creating kudos"""
        request = self.context.get('request')
        if request and hasattr(request, 'user_id'):
            sender_id = request.user_id
            receiver_id = data.get('receiver').id
            
            # Check if trying to send to self
            if sender_id == receiver_id:
                raise serializers.ValidationError("You cannot give kudos to yourself.")
            
            # Check if sender has remaining kudos
            try:
                sender = User.objects.get(id=sender_id)
                if sender.get_remaining_kudos() <= 0:
                    raise serializers.ValidationError("You have no remaining kudos for this week.")
                
                # Check if sender and receiver are in the same organization
                receiver = data.get('receiver')
                if sender.organization != receiver.organization:
                    raise serializers.ValidationError("You can only give kudos to users in your organization.")
                    
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid sender.")
        
        return data
