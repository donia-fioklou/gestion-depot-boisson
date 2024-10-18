from rest_framework import serializers

from gest_stock_app.models.DetailConsignation import DetailConsignation

class DetailConsignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailConsignation
        fields = '__all__'