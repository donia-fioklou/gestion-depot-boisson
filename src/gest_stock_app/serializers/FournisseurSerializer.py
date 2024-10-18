from rest_framework import serializers

from gest_stock_app.models.Fournisseur import Fournisseur


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'