'''from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.db import transaction
from gest_stock_app.models.Client import Client
from gest_stock_app.models.Consignation import Consignation

# Capture l'ancienne quantité de consignation avant la mise à jour
@receiver(pre_save, sender=Consignation)
def capture_old_qte_consignation(sender, instance, **kwargs):
    # Cette opération ne doit se faire que si l'instance existe déjà (mise à jour)
    if instance.pk and not instance._state.adding:
        # Récupérer l'ancienne consignation avant la mise à jour
        ancienne_consignation = Consignation.objects.get(pk=instance.pk)
        instance._ancienne_qte_casier = ancienne_consignation.qte_casier
        instance._ancienne_qte_bouteille = ancienne_consignation.qte_bouteille if ancienne_consignation.qte_bouteille else 0
    else:
        instance._ancienne_qte_casier = None
        instance._ancienne_qte_bouteille = None

# Met à jour les quantités de consignation du client lors de la sauvegarde d'une consignation
@receiver(post_save, sender=Consignation)
@transaction.atomic
def update_client_consignation_on_save(sender, instance, created, **kwargs):
    client = instance.client
    
    if created:
        # Si c'est une nouvelle consignation
        print('create consignation')
        if instance.type_consignation == 1:  # Emprunt
            client.qte_consignation_ca += instance.qte_casier
            client.qte_consignation_btle += instance.qte_bouteille or 0
        elif instance.type_consignation == 2:  # Retour
            if client.qte_consignation_ca >= instance.qte_casier:
                client.qte_consignation_ca -= instance.qte_casier
            else:
                raise ValueError("La quantité de casiers retournés est supérieure à celle en consignation.")

            if client.qte_consignation_btle >= (instance.qte_bouteille or 0):
                client.qte_consignation_btle -= instance.qte_bouteille or 0
            else:
                raise ValueError("La quantité de bouteilles retournées est supérieure à celle en consignation.")
    
    else:
        # Si c'est une mise à jour
        print('update consignation')
        ancienne_qte_casier = instance._ancienne_qte_casier if instance._ancienne_qte_casier is not None else 0
        ancienne_qte_bouteille = instance._ancienne_qte_bouteille if instance._ancienne_qte_bouteille is not None else 0

        # Mise à jour des quantités de casiers et bouteilles
        difference_qte_casier = instance.qte_casier - ancienne_qte_casier
        difference_qte_bouteille = (instance.qte_bouteille or 0) - ancienne_qte_bouteille

        if instance.type_consignation == 1:  # Emprunt
            client.qte_consignation_ca += difference_qte_casier
            client.qte_consignation_btle += difference_qte_bouteille
        elif instance.type_consignation == 2:  # Retour
            if client.qte_consignation_ca >= difference_qte_casier:
                client.qte_consignation_ca -= difference_qte_casier
            else:
                raise ValueError("La quantité de casiers retournés est supérieure à celle en consignation.")

            if client.qte_consignation_btle >= difference_qte_bouteille:
                client.qte_consignation_btle -= difference_qte_bouteille
            else:
                raise ValueError("La quantité de bouteilles retournées est supérieure à celle en consignation.")
    
    client.save()

# Met à jour les quantités de consignation du client lors de la suppression d'une consignation
@receiver(pre_delete, sender=Consignation)
@transaction.atomic
def update_client_consignation_on_delete(sender, instance, **kwargs):
    client = instance.client
    if instance.type_consignation == 1:  # Suppression d'un emprunt
        client.qte_consignation_ca -= instance.qte_casier
        client.qte_consignation_btle -= instance.qte_bouteille or 0
    elif instance.type_consignation == 2:  # Suppression d'un retour
        client.qte_consignation_ca += instance.qte_casier
        client.qte_consignation_btle += instance.qte_bouteille or 0
    
    client.save()


    
'''