from rest_framework import serializers

from gest_stock_app.models.Stock import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'