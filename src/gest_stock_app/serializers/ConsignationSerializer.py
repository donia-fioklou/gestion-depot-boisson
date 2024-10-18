from rest_framework import serializers

from gest_stock_app.models.Consignation import Consignation

class ConsignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignation
        fields = '__all__'