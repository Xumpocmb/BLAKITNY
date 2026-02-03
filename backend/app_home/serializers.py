from rest_framework import serializers
from .models import Slider, CompanyDetails, SiteLogo, SocialNetwork


class SliderSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Slider
        fields = ['id', 'image_url', 'alt_text']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ['id', 'name', 'description']


class SiteLogoSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteLogo
        fields = ['id', 'logo_url', 'created_at', 'updated_at']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo:
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class SocialNetworkSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = SocialNetwork
        fields = ['id', 'name', 'icon_url', 'link', 'is_active']

    def get_icon_url(self, obj):
        request = self.context.get('request')
        if obj.icon:
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None