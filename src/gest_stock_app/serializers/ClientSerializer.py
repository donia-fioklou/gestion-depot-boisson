from rest_framework import serializers

from gest_stock_app.serializers.ConsignationSerializer import ConsignationSerializer
from gest_stock_app.models.Client import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ClientDetailSerializer(serializers.ModelSerializer):
    consignation = serializers.SerializerMethodField()


    class Meta:
        model = Client
        fields = ["id","nom","adresse","qte_consignation_ca","qte_consignation_btle","consignation"]
    def get_consignation(self, instance):
        queryset = instance.consignation.filter(is_deleted=False).order_by('-date_modification')
        serializer = ConsignationSerializer(queryset, many=True)
        return serializer.data