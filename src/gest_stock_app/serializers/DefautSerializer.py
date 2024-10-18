from rest_framework import serializers

from gest_stock_app.models.Defaut import Defaut

class DefautSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defaut
        fields = '__all__'