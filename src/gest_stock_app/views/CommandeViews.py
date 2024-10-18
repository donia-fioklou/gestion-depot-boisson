from rest_framework import viewsets,status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from gest_stock_app.models.Commande import Commande
from gest_stock_app.serializers.CommandeSerializer import CommandeDetailSerializer, CommandeSerializer
from gest_stock_app.views.MultipleSerializerMixin import MultipleSerializerMixin

class CommandeViewSet(MultipleSerializerMixin,viewsets.ModelViewSet):
    serializer_class = CommandeSerializer
    detail_serializer_class = CommandeDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retourne seulement les commandes qui ne sont pas supprimées
        return Commande.objects.filter(is_deleted=False).order_by('-date_creation')

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        self.get_object().delete()
        return Response()