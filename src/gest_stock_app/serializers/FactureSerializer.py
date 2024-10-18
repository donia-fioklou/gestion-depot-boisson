from rest_framework import serializers

from gest_stock_app.models.Facture import Facture

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = '__all__'