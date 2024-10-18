from rest_framework import serializers

from gest_stock_app.models.Produit import Produit


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'