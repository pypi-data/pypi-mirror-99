"""
    Serializer for Degreed configuration.
"""
from rest_framework import serializers

from integrated_channels.degreed.models import DegreedEnterpriseCustomerConfiguration


class DegreedConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreedEnterpriseCustomerConfiguration
        fields = '__all__'
