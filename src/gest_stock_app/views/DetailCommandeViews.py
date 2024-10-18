from rest_framework import viewsets,status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gest_stock_app.models.HistoriqueStock import HistoriqueStock
from gest_stock_app.models.DetailCommande import DetailCommande
from gest_stock_app.serializers.DetailCommandeSerializer import DetailCommandeSerializer

class DetailCommandeViewSet(viewsets.ModelViewSet):
    queryset = DetailCommande.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = DetailCommandeSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()
        # Réduction du stock en fonction de la quantité supprimée
        instance.produit.qte_casier -= instance.qte_casier
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=-instance.qte_casier,
            mouvement_type="suppression detail commande",
            utilisateur=None
        )
        instance.produit.save()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)