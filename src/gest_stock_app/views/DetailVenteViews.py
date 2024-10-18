from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gest_stock_app.models.HistoriqueStock import HistoriqueStock
from gest_stock_app.models.DetailVente import DetailVente
from gest_stock_app.serializers.DetailsVenteSerializer import DetailVenteSerializer

class DetailVenteViewSet(viewsets.ModelViewSet):
    queryset = DetailVente.objects.filter(is_deleted=False).order_by('-date_modification')
    serializer_class = DetailVenteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()
        # augmentatio du stock en fonction de la quantité supprimée
        instance.produit.qte_casier += instance.qte_casier
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=-instance.qte_casier,
            mouvement_type="suppression detail vente",
            utilisateur=None
        )
        instance.produit.save()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)