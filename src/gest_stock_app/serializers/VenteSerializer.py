from rest_framework import serializers

from gest_stock_app.models.Vente import Vente
from gest_stock_app.serializers.DetailsVenteSerializer import DetailVenteSerializer

class VenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vente
        fields = '__all__'

class VenteDetailSerializer(serializers.ModelSerializer):
    detailVente=serializers.SerializerMethodField()
    class Meta:
        model = Vente
        fields = ["id","code","type_vente","date","client","remise","detailVente"]
    
    def get_detailVente(self,instance):
        queryset = instance.detailVente.filter(is_deleted=False)
        serializer = DetailVenteSerializer(queryset, many=True)
        return serializer.data