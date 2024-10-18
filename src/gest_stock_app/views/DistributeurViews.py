from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gest_stock_app.models.Distributeur import Distributeur
from gest_stock_app.serializers.DistributeurSerializer import DistributeurSerializer


class DistributeurViewSet(viewsets.ModelViewSet):
    queryset = Distributeur.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = DistributeurSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)