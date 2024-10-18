from django.apps import AppConfig


class GestStockAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gest_stock_app'

    def ready(self):
        import gest_stock_app.signals.ProduitSignals
        #import gest_stock_app.signals.consignationSignals
        