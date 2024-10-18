from rest_framework import serializers

from gest_stock_app.models.TypeConsignation import TypeConsignation

class TypeConsignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeConsignation
        fields = '__all__'