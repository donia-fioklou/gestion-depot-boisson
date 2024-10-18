# signals pour mettre a jour le stock
from django.db.models.signals import post_save, pre_delete,pre_save,post_delete
from django.dispatch import receiver
from django.db import transaction

from gest_stock_app.models.HistoriqueStock import HistoriqueStock
from gest_stock_app.models.Produit import Produit
from gest_stock_app.models.DetailCommande import DetailCommande
from gest_stock_app.models.DetailVente import DetailVente

@receiver(pre_save, sender=DetailCommande)
def capture_old_qte_casier_commande(sender, instance, **kwargs):
    # Cette opération ne doit se faire que si l'instance existe déjà (mise à jour)
    if instance.pk and not instance._state.adding:
        # Récupérer l'ancienne commande avant la mise à jour
        ancienne_commande = DetailCommande.objects.get(pk=instance.pk)
        instance._ancienne_qte_casier = ancienne_commande.qte_casier
    else:
        instance._ancienne_qte_casier = None
@receiver(post_save, sender=DetailCommande)
@transaction.atomic
def update_stock_on_commande_save(sender, instance, created, **kwargs):
    print("created",created)
    if created:
        print('create')
        instance.produit.qte_casier += instance.qte_casier
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=instance.qte_casier,
            mouvement_type="commande",
            utilisateur=None  
        )
    else:
        print('update')
        # Mise à jour d'une commande existante
       
        ancienne_qte_casier = instance._ancienne_qte_casier if instance._ancienne_qte_casier is not None else 0
        
        difference_qte = instance.qte_casier - ancienne_qte_casier
        print('ancien',ancienne_qte_casier)
        print('nouveau', instance.qte_casier)
        instance.produit.qte_casier += difference_qte
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=difference_qte,
            mouvement_type="modification de commande",
            utilisateur=None
        )
    instance.produit.save()

@receiver(post_delete, sender=DetailCommande)
@transaction.atomic
def update_stock_on_commande_delete(sender, instance, **kwargs):
    print('delete')
    # Réduction du stock en fonction de la quantité supprimée
    instance.produit.qte_casier -= instance.qte_casier
    HistoriqueStock.objects.create(
        produit=instance.produit,
        qte_change=-instance.qte_casier,
        mouvement_type="suppression de commande",
        utilisateur=None
    )
    instance.produit.save()


@receiver(pre_save, sender=DetailVente)
def capture_old_qte_casier_vente(sender, instance, **kwargs):
    # Cette opération ne doit se faire que si l'instance existe déjà (mise à jour)
    if instance.pk and not instance._state.adding:
        # Récupérer l'ancienne vente avant la mise à jour
        ancienne_vente = DetailVente.objects.get(pk=instance.pk)
        instance._ancienne_qte_casier = ancienne_vente.qte_casier
    else:
        instance._ancienne_qte_casier = None
        
@receiver(post_save, sender=DetailVente)
@transaction.atomic
def update_stock_on_vente_save(sender, instance, created, **kwargs):
    if created:
        print('create')
        if instance.produit.qte_casier < instance.qte_casier:
            raise ValueError("La quantité à vendre est supérieure à la quantité en stock.")
        instance.produit.qte_casier -= instance.qte_casier
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=-instance.qte_casier,
            mouvement_type="vente",
            utilisateur=None
        )
    else:
        print('update')

        ancienne_qte_casier = instance._ancienne_qte_casier if instance._ancienne_qte_casier is not None else 0
        difference_qte = instance.qte_casier - ancienne_qte_casier
        if instance.produit.qte_casier < difference_qte:
            raise ValueError("La quantité à vendre est supérieure à la quantité en stock.")
        instance.produit.qte_casier -= difference_qte
        HistoriqueStock.objects.create(
            produit=instance.produit,
            qte_change=-difference_qte,
            mouvement_type="modification de vente",
            utilisateur=None
        )
    instance.produit.save()

@receiver(pre_delete, sender=DetailVente)
@transaction.atomic
def update_stock_on_vente_delete(sender, instance, **kwargs):
    instance.produit.qte_casier += instance.qte_casier
    instance.produit.save()
    HistoriqueStock.objects.create(
        produit=instance.produit,
        qte_change=instance.qte_casier,
        mouvement_type="suppression de vente",
        utilisateur=None
    )


