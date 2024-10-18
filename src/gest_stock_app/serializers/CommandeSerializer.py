from rest_framework import serializers

from gest_stock_app.models.Commande import Commande
from gest_stock_app.serializers.DetailCommandeSerializer import DetailCommandeSerializer


class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class CommandeDetailSerializer(serializers.ModelSerializer):
    detailCommande = serializers.SerializerMethodField()
    class Meta:
        model = Commande
        # all fields with detail commande
        fields = ["id","code","date","type_transport","frais_transport","mt_total","distributeur","detailCommande"]  

    def get_detailCommande(self, instance):
        queryset = instance.detailCommande.filter(is_deleted=False)
        serializer =  DetailCommandeSerializer(queryset, many=True)
        return serializer.data