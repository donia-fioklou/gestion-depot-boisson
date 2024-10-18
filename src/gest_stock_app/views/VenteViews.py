from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from gest_stock_app.models.Vente import Vente
from gest_stock_app.serializers.VenteSerializer import VenteDetailSerializer, VenteSerializer
from gest_stock_app.views.MultipleSerializerMixin import MultipleSerializerMixin

class VenteViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
    serializer_class = VenteSerializer
    detail_serializer_class = VenteDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vente.objects.filter(is_deleted=False).order_by('-date_creation')

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        self.get_object().delete()
        return Response()


class VenteFilterByDateViewSet(APIView):

    def post(self, request):
        date = request.data.get('date')
        ventes = Vente.objects.filter(date=date)
        serializer = VenteDetailSerializer(ventes, many=True)
        return Response(serializer.data)
    