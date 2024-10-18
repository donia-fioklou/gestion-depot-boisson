from rest_framework import serializers

from gest_stock_app.models.Distributeur import Distributeur


class DistributeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributeur
        fields = '__all__'