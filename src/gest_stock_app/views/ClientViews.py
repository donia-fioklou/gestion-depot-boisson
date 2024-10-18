from rest_framework import viewsets,status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from gest_stock_app.models.Client import Client
from gest_stock_app.serializers.ClientSerializer import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = ClientSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)