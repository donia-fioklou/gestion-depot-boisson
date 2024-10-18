from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from gest_stock_app.models.Client import Client
from gest_stock_app.serializers.ClientSerializer import ClientDetailSerializer
from gest_stock_app.models.Consignation import Consignation
from gest_stock_app.serializers.ConsignationSerializer import ConsignationSerializer

class ConsignationViewSet(viewsets.ModelViewSet):
    queryset = Consignation.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = ConsignationSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()

        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsignationGroupeByClient(APIView):
    def get(self, request, *args, **kwargs):
        # Filtrer uniquement les clients qui ont au moins une consignation non supprimée
        clients = Client.objects.filter(consignation__is_deleted=False).distinct()
        
        # Si tu souhaites inclure tous les clients, même ceux sans consignation, tu peux omettre cette ligne
        # clients = Client.objects.all()

        # Sérialiser les clients avec leurs consignations
        serializer = ClientDetailSerializer(clients, many=True)
        
        # Retourner les données sous forme de réponse JSON
        return Response(serializer.data, status=status.HTTP_200_OK)