from rest_framework import serializers

from gest_stock_app.models.DetailCommande import DetailCommande


class DetailCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCommande
        fields = '__all__'