from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gest_stock_app.views.ClientViews import ClientViewSet
from gest_stock_app.views.CommandeViews import CommandeViewSet
from gest_stock_app.views.ConsignationViews import ConsignationGroupeByClient, ConsignationViewSet
from gest_stock_app.views.DetailConsignationViews import DetailConsignationViewSet
from gest_stock_app.views.DefautViews import DefautViewSet
from gest_stock_app.views.DetailCommandeViews import DetailCommandeViewSet
from gest_stock_app.views.DetailVenteViews import DetailVenteViewSet
from gest_stock_app.views.FactureViews import FactureViewSet, GenrateFacturePdfView
from gest_stock_app.views.DistributeurViews import DistributeurViewSet
from gest_stock_app.views.FournisseurViews import FournisseurViewSet
from gest_stock_app.views.ProduitViews import ProduitViewSet
from gest_stock_app.views.TypeCasierViews import TypeCasierViewSet
from gest_stock_app.views.VenteViews import VenteFilterByDateViewSet, VenteViewSet
from gest_stock_app.views.statistiquesViews import StatisticNumberOfSaleViews,StatisticNumberOfOrdersViews,StatisticTotalAmountSaleViews,StatisticTotalAmountOrderViews,StatisticNumberOfConsignation,StatisticNumberCasierSoldViews

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('commandes', CommandeViewSet,basename='commandes')
router.register('consignations', ConsignationViewSet, basename='consignations')
router.register('detail-consignations', DetailConsignationViewSet)
router.register('defauts', DefautViewSet)
router.register('detail-commandes', DetailCommandeViewSet)
router.register('detail-ventes', DetailVenteViewSet)
router.register('factures', FactureViewSet)
router.register('fournisseurs', FournisseurViewSet)
router.register('distributeurs', DistributeurViewSet)
router.register('produits', ProduitViewSet)
router.register('types-casiers', TypeCasierViewSet)
router.register('ventes', VenteViewSet,basename='ventes')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-facture-pdf/<str:id_vente>/', GenrateFacturePdfView.as_view(), name='genrate-facture-pdf'),
    path('vente-filter-by-date/', VenteFilterByDateViewSet.as_view(), name='vente-filter-by-date'),
    path('statistic-number-of-sale/', StatisticNumberOfSaleViews.as_view(), name='statistic-number-of-sale'),
    path('statistic-number-of-order/', StatisticNumberOfOrdersViews.as_view(), name='statistic-number-of-order'),
    path('statistic-total-amount-of-order/',StatisticTotalAmountOrderViews.as_view(),name='statistic-total-amount-of-order'),
    path('statistic-total-amount-of-sale/', StatisticTotalAmountSaleViews.as_view(), name='statistic-total-amount-of-sale'),
    path('statistic-number-casier-sold/', StatisticNumberCasierSoldViews.as_view(), name='statistic-number-casier-sold'),
    path('statistic-number-of-consignation/', StatisticNumberOfConsignation.as_view(), name='statistic-number-of-consignation'),
    path('consignation-group-by-client/', ConsignationGroupeByClient.as_view(), name='consignation-group-by-client'),


]
