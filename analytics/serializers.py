from rest_framework import serializers

from analytics.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"
