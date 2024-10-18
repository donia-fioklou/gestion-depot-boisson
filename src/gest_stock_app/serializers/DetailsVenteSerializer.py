from rest_framework import serializers

from gest_stock_app.models.DetailVente import DetailVente

class DetailVenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailVente
        fields = '__all__'