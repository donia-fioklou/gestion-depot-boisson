

class Helper():

    def format_price(value):
        return "{:,.0f}".format(float(value)).replace(",", " ")


    def get_qte_casier(qte_casier):
            #partie entier de qte_casier
            return int(qte_casier)
            
    def get_qte_bouteille(taille_casier,qte_casier):
        #partie decimal de qte_casier
        qte_casier_decimal = float(qte_casier) % 1
        #nbre btle
        return int(round(taille_casier * qte_casier_decimal,2))
         

    #calcul du prix total d'un detail vente
    def get_total_detail_vente(detail_vente):
        taille_casier = detail_vente.produit.type_casier.taille
        prix_casier = detail_vente.produit.pu_casier * Helper.get_qte_casier(detail_vente.qte_casier)
        prix_bouteille = float(detail_vente.produit.pu_bouteille) * Helper.get_qte_bouteille(taille_casier,detail_vente.qte_casier)
        totale_detail_vente = float(prix_casier) + prix_bouteille
        return totale_detail_vente 


    ##calcul du prix total d'un detail commande
    def get_total_detail_commande(detail_commande):
        totale_detail_commande = detail_commande.produit.prix_achat_casier * detail_commande.qte_casier
        return totale_detail_commande
    

