from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from gest_stock_app.models.DetailVente import DetailVente
from gest_stock_app.models.Facture import Facture
from gest_stock_app.models.Vente import Vente
from gest_stock_app.serializers.FactureSerializer import FactureSerializer
from django.http import HttpResponse

from reportlab.lib.pagesizes import A5
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.http import FileResponse
import os
import uuid

from gest_stock_app.views.Helper import Helper


class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.filter(is_deleted=False)
    serializer_class = FactureSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """ Effectue une suppression logique """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
#generer facture pdf
class GenrateFacturePdfView(APIView):

    # Ajustement des marges pour A5
    margin_left = 1 * cm
    margin_right = A5[0] - margin_left
    margin_top = A5[1] - 1.5 * cm
    margin_bottom = 1.5 * cm

    permission_classes = [IsAuthenticated]

    def taille_casier(self,detail_vente):
        produit = detail_vente.produit
        type_casier_taille = produit.type_casier.taille
        return type_casier_taille


    def handle_facture_data(self, vente):
        detail_ventes = DetailVente.objects.filter(vente=vente,is_deleted=False)
        liste_detail_ventes = []

        remise = vente.remise
        total_vente = 0
        total_casier = 0
        total_btle = 0

        for detail_vente in detail_ventes :
            total_casier += Helper.get_qte_casier(detail_vente.qte_casier)
            total_btle += Helper.get_qte_bouteille(self.taille_casier(detail_vente),detail_vente.qte_casier)

            total_detail_vente = Helper.get_total_detail_vente(detail_vente)
            liste_detail_ventes.append({
                'boisson': detail_vente.produit.nom,
                'type_casier': self.taille_casier(detail_vente),
                'qte_casiers': Helper.get_qte_casier(detail_vente.qte_casier),
                'qte_bouteilles' : Helper.get_qte_bouteille(self.taille_casier(detail_vente),detail_vente.qte_casier),
                'prix_unitaire_casier': Helper.format_price(detail_vente.produit.pu_casier),
                'prix_unitaire_bouteille': Helper.format_price(detail_vente.produit.pu_bouteille),
                'total': Helper.format_price(total_detail_vente)
            })
            total_vente += Helper.get_total_detail_vente(detail_vente)
        return {
            'id': vente.id,
            'code': vente.code,
            'date': vente.date,
            'client_name': vente.client.nom,
            'client_address': vente.client.adresse,
            'liste_detail_ventes': liste_detail_ventes,
            'total_casier':total_casier,
            'total_btle':total_btle,
            'remise': remise,
            'total_vente': Helper.format_price(total_vente), 
            'mt_net' : Helper.format_price(total_vente - int(remise))
        }
    
    def header_invoice(self,c,nom_caisier,vente_code,vente_date,client_name):
        # Info du fournisseur en haut à gauche en trois lignes
        c.setFont("Helvetica", 10)
        c.drawString(self.margin_left, self.margin_top, "DEPOT BKB DISTRIBUTION")
        c.drawString(self.margin_left, self.margin_top - 12, "Distributeur des produits BB et SNB")
        c.drawString(self.margin_left, self.margin_top - 24, "Tel 93 60 72 26/79 85 19 99")
        c.drawString(self.margin_left, self.margin_top - 36, "LOME - TOGO")

        # Titre FACTURE après info fournisseur au centre
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(A5[0] / 2, self.margin_top - 60, "FACTURE")

        # Nom du caissier à gauche
        c.setFont("Helvetica", 10)
        c.drawString(self.margin_left, self.margin_top - 84, f"Caissier : {nom_caisier}")

        # Code vente à gauche en bas du nom du caissier
        c.drawString(self.margin_left, self.margin_top - 96, f"Ref : {vente_code}")

        # Date vente à droite
        c.drawString(self.margin_right-100, self.margin_top - 84, f"Date : {vente_date}")

        # Nom client à droite en bas de la date vente
        c.drawString(self.margin_right-100, self.margin_top - 96, f"Client : {client_name}")

    def generate_facture_pdf(self, vente,user):
        vente_data = self.handle_facture_data(vente)
        filename = f"{uuid.uuid4()}_vente_{vente_data['code']}.pdf"
        document_title = f"Facture de Vente #{vente_data['code']}"
        page_title = "Détails de la Vente"
        client_name = vente_data["client_name"]
        client_address = vente_data["client_address"]
        total_vente = vente_data["total_vente"]
        detail_ventes = vente_data["liste_detail_ventes"]
        vente_date = vente_data["date"]
        vente_code = vente_data["code"]
        vente_remise = vente_data["remise"]
        vente_mt_net = vente_data["mt_net"]
        vente_total_casier = vente_data["total_casier"]
        vente_total_btle = vente_data["total_btle"]

        nom_caisier = f"{user.last_name} {user.first_name}"

        # Créer un dossier facture s'il n'existe pas 
        if not os.path.exists('facture'):
            os.makedirs('facture')
        # Créer le chemin du fichier pdf dans le dossier facture
        pdf_file_path = os.path.join('facture', filename)

        # Création du canvas pdf dans le dossier facture
        c = canvas.Canvas(pdf_file_path, pagesize=A5)


        # Tableau des produits en utilisant Table
        table_headers = ["Articles",  "Qté Cas", "Qté Btl sp","PU Casier","PU Bouteille",   "Total"]
        data = [table_headers]

        
        for detail in detail_ventes:

            data.append([
                f"{detail["boisson"]} C {detail["type_casier"]}",
                #detail["type_casier"],
                detail["qte_casiers"],
                detail["qte_bouteilles"],
                detail["prix_unitaire_casier"],
                detail["prix_unitaire_bouteille"],
                detail["total"]
            ])
        
        
        rows_per_page = 17
        chunks = [data[i:i + rows_per_page] for i in range(0, len(data), rows_per_page)]
        for i, chunk in enumerate(chunks):
            self.header_invoice(c, nom_caisier, vente_code, vente_date, client_name)

            # Création du tableau dans le PDF
            table = Table(chunk, colWidths=[3.75 * cm,  1.25 * cm, 1.5 * cm, 2 * cm, 2 * cm, 3 * cm])
            table_style = TableStyle([
                #('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Taille de la police pour tout le tableau (réduite à 8)
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                #('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ])
            table.setStyle(table_style)
            
            # Positionnement du tableau sur la page
            table_width, table_height = table.wrap(self.margin_right - self.margin_left, self.margin_bottom)
            table.drawOn(c, self.margin_left, self.margin_top-table_height - 110)
            # dessiner le total et les sections de signature en dessous du dernier tableau
            if i == len(chunks) - 1:
                table_recap_data = [["Total Casier"],[vente_total_casier],
                                    ["Total Bouteille"],[vente_total_btle]]
                
                table_recap_style = TableStyle([
                #('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Taille de la police pour tout le tableau (réduite à 8)
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                #('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ])

                table_recap = Table(table_recap_data, colWidths=[ 3.75 * cm])
                table_recap.setStyle(table_recap_style)
                
                table_recap_width, table_recap_height = table_recap.wrap(self.margin_right - self.margin_left, self.margin_bottom)
                table_recap.drawOn(c, self.margin_left, self.margin_top-table_height -207)

                table_recap_price = [["Montant total"],[total_vente],
                                     ["Remise"],[vente_remise],
                                    ["Net à payer"],[vente_mt_net]]
                table_style_price = TableStyle([
                #('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
                ('FONTNAME', (0, 4), (-1, 5), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Taille de la police pour tout le tableau (réduite à 8)
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                #('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ])
                table_recap_price = Table(table_recap_price, colWidths=[3 * cm])
                table_recap_price.setStyle(table_style_price)
                table_recap_price_width, table_recap_price_height = table_recap_price.wrap(self.margin_right - self.margin_left, self.margin_bottom)
                table_recap_price.drawOn(c, self.margin_right-65, self.margin_top-table_height -243)

                # # Positionner le total juste en dessous du tableau
                # c.setFont("Helvetica-Bold", 10)
                # c.drawString(self.margin_right-100, self.margin_top - 120 - table_height - 20, f"Total: {total_vente} CFA")

                # Ajouter les sections de signature en dessous du total
                c.setFont("Helvetica", 10)
                c.drawString(self.margin_left, self.margin_top - table_height - table_recap_price_height- 150, "Signature Caissier:")
                #c.line(self.margin_left, self.margin_top - 120 - table_height - 50, self.margin_left + 150, self.margin_top - 120 - table_height - 50)
                c.drawString(self.margin_right - 100, self.margin_top - table_height- table_recap_price_height - 150, "Signature Client:")
                #c.line(self.margin_right - 150, self.margin_top - 120 - table_height - 50, self.margin_right, self.margin_top - 120 - table_height - 50)
            
            
            c.showPage()
        

        c.save()
        path = os.path.join(os.getcwd(), pdf_file_path) 
        return path


    def get(self, request, id_vente):
        vente = Vente.objects.get(id=id_vente)
        user = request.user
        '''#enregistrer facture dans la base de données
        facture = Facture.objects.create(
            vente=vente,
            reference=f"Facture_{vente.code}",  # Generate a reference
            file_path=pdf_data['file_path']  # Store the PDF path
        )'''
        
        # Générer le PDF de la facture
        pdf_path = self.generate_facture_pdf(vente,user)
        if os.path.exists(pdf_path):
            response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            return response
        return Response({"error": "File not found."}, status=404)
