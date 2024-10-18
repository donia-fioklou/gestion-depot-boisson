from rest_framework import serializers

from gest_stock_app.models.TypeCasier import TypeCasier


class TypeCasierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCasier
        fields = '__all__'