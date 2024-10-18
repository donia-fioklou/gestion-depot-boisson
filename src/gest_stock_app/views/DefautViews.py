from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gest_stock_app.models.Defaut import Defaut
from gest_stock_app.serializers.DefautSerializer import DefautSerializer

class DefautViewSet(viewsets.ModelViewSet):
    queryset = Defaut.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = DefautSerializer

    permission_classes = [IsAuthenticated]