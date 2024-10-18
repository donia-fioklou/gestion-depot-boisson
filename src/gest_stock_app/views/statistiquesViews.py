from rest_framework.views import APIView
from gest_stock_app.models.Commande import Commande
from gest_stock_app.models.Consignation import Consignation
from gest_stock_app.models.DetailCommande import DetailCommande
from gest_stock_app.models.DetailVente import DetailVente
from gest_stock_app.models.Produit import Produit
from gest_stock_app.models.Vente import Vente
from rest_framework.response import Response
from django.db.models import Count


from gest_stock_app.views.Helper import Helper
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class HelperStatictic():
    @staticmethod
    def fill_missing_dates(object_list, start_date, periods, unit):
        print('object_list',object_list)

        # Helper method to ensure all dates are filled, even if object_list are missing for some days/months/years.
        result = []
        if unit == 'days':
            # Si on utilise les jours, on a déjà une clé 'date' dans les ventes
            object_list_dict = {entry['date'].strftime('%Y-%m-%d'): entry['count_number'] for entry in object_list}
        elif unit == 'months':
            # Pour les mois, il faut reconstituer la clé basée sur année et mois
            object_list_dict = {f"{entry['month']}": entry['count_number'] for entry in object_list}
        elif unit == 'years':
            # Pour les années, on utilise simplement l'année
            object_list_dict = {str(entry['year']): entry['count_number'] for entry in object_list}

        for i in range(periods):
            if unit == 'days':
                current_date = start_date + datetime.timedelta(days=i)
                date_key = str(current_date)
            elif unit == 'months':
                current_date = (start_date + relativedelta(months=i)).replace(day=1)
                date_key = f"{current_date.year}-{str(current_date.month).zfill(2)}"

            elif unit == 'years':
                current_date = start_date + relativedelta(years=i)
                date_key = str(current_date.year)
                print('date_key', date_key)

            result.append({
                'date': date_key,
                'count_number': object_list_dict.get(date_key, 0)
            })



        return result
    
    @staticmethod
    def get_last_7_days():
        today = timezone.now().date()
        return today - datetime.timedelta(days=6)

    @staticmethod
    def get_last_12_months():
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        # Remonter de 11 mois pour inclure le mois actuel dans les 12 derniers mois
        start_date = start_of_month - relativedelta(months=11)
        return start_date

    @staticmethod
    def get_last_5_years():
        today = timezone.now().date()
        return today.replace(year=today.year - 4, month=1, day=1)
class StatisticNumberOfSaleViews(APIView):

    """
    View to get the number of sales based on period (week, months, years).
    
    - `Week`: 1, return list of last 7 days with number of sales associated.
    - `Months`: 2, return list of last 12 months with number of sales associated.
    - `Years`: 3, return list of last 5 years with number of sales associated.
    """

    def get_list_of_number_of_sale_base_on_periode(self, periode):
        sales = Vente.objects.filter(is_deleted=False)

        if periode == 1:
            start_date = HelperStatictic.get_last_7_days()
            sales = sales.filter(date__gte=start_date).extra({'date': "date(date)"}).values('date').annotate(count_number=Count('id')).order_by('date')
            result = HelperStatictic.fill_missing_dates(sales, start_date, 7, 'days')

        elif periode == 2:
            start_date = HelperStatictic.get_last_12_months()
            sales = sales.filter(date__gte=start_date).extra({'month': "EXTRACT(YEAR FROM date) || '-' || LPAD(EXTRACT(MONTH FROM date)::text, 2, '0')"}).values('month').annotate(count_number=Count('id')).order_by('month')
            print('sales 2', sales)
            result = HelperStatictic.fill_missing_dates(sales, start_date, 12, 'months')

        elif periode == 3:
            start_date = HelperStatictic.get_last_5_years()
            sales = sales.filter(date__gte=start_date).extra({'year': "EXTRACT(year FROM date)"}).values('year').annotate(count_number=Count('id')).order_by('year')
            result = HelperStatictic.fill_missing_dates(sales, start_date, 5, 'years')

        return result
            
    
        
    def post(self, request):
        periode = int(request.data.get('periode'))
        result = self.get_list_of_number_of_sale_base_on_periode(periode)
        return Response({"data": result})

class StatisticNumberOfOrdersViews(APIView):
    """
    View to get the number of orders based on period (week, months, years).
    
    - `Week`: 1, return list of last 7 days with number of orders associated.
    - `Months`: 2, return list of last 12 months with number of orders associated.
    - `Years`: 3, return list of last 5 years with number of orders associated.
    """

    def get_list_of_number_of_orders_base_on_periode(self, periode):
        orders = Commande.objects.filter(is_deleted=False)

        if periode == 1:
            start_date = HelperStatictic.get_last_7_days()
            orders = orders.filter(date__gte=start_date).extra({'date': "date(date)"}).values('date').annotate(count_number=Count('id')).order_by('date')
            result = HelperStatictic.fill_missing_dates(orders, start_date, 7, 'days')

        elif periode == 2:
            start_date = HelperStatictic.get_last_12_months()
            orders = orders.filter(date__gte=start_date).extra({'month': "EXTRACT(YEAR FROM date) || '-' || LPAD(EXTRACT(MONTH FROM date)::text, 2, '0')"}).values('month').annotate(count_number=Count('id')).order_by('month')
            print('orders 2', orders)
            result = HelperStatictic.fill_missing_dates(orders, start_date, 12, 'months')

        elif periode == 3:
            start_date = HelperStatictic.get_last_5_years()
            orders = orders.filter(date__gte=start_date).extra({'year': "EXTRACT(year FROM date)"}).values('year').annotate(count_number=Count('id')).order_by('year')
            result = HelperStatictic.fill_missing_dates(orders, start_date, 5, 'years')

        return result
            
    def post(self, request):
        periode = int(request.data.get('periode'))
        result = self.get_list_of_number_of_orders_base_on_periode(periode)
        return Response({"data": result})

class StatisticTotalAmountSaleViews(APIView):
    """
    View to get the total amount of sales based on period (week, months, years).
    
    - `Week`: 1, return list of last 7 days with total amount of sales associated.
    - `Months`: 2, return list of last 12 months with total amount of sales associated.
    - `Years`: 3, return list of last 5 years with total amount of sales associated.
    """

    def get_total_amount_sales_by_period(self, periode, product_id=None):
        sales = Vente.objects.filter(is_deleted=False)

        total_amounts = []

        if periode == 1:
            start_date = HelperStatictic.get_last_7_days()
            sales = sales.filter(date__gte=start_date)

            for i in range(7):
                day_date = start_date + datetime.timedelta(days=i)
                sales_for_day = sales.filter(date=day_date)
                total_amount = 0

                for sale in sales_for_day:
                    total_amount += self.get_total_amount_for_sale(sale, product_id)

                total_amounts.append({
                    'date': str(day_date),
                    'total_amount': total_amount
                })

        elif periode == 2:
            start_date = HelperStatictic.get_last_12_months()
            for i in range(12):
                month_date = (start_date + relativedelta(months=i)).replace(day=1)
                sales_for_month = sales.filter(date__year=month_date.year, date__month=month_date.month)
                total_amount = 0

                for sale in sales_for_month:
                    total_amount += self.get_total_amount_for_sale(sale, product_id)

                total_amounts.append({
                    'date': f"{month_date.year}-{str(month_date.month).zfill(2)}",
                    'total_amount': total_amount
                })

        elif periode == 3:
            start_date = HelperStatictic.get_last_5_years()
            for i in range(5):
                year_date = start_date.replace(year=start_date.year + i)
                sales_for_year = sales.filter(date__year=year_date.year)
                total_amount = 0

                for sale in sales_for_year:
                    total_amount += self.get_total_amount_for_sale(sale, product_id)

                total_amounts.append({
                    'date': str(year_date.year),
                    'total_amount': total_amount
                })

        return total_amounts

    def get_total_amount_for_sale(self, sale, product_id=None):
        total_amount = 0
        if product_id:
            detail_sale = DetailVente.objects.filter(is_deleted=False, vente=sale, produit=product_id)
        else:
            detail_sale = DetailVente.objects.filter(is_deleted=False, vente=sale)

        for detail in detail_sale:
            total_amount += Helper.get_total_detail_vente(detail)
        if sale.remise:
            total_amount -= int(sale.remise)
        return total_amount

    def post(self, request):
        periode = int(request.data.get('periode'))
        product_id = request.data.get('product_id', None)
        result = self.get_total_amount_sales_by_period(periode, product_id)
        return Response({"data": result})
class StatisticNumberCasierSoldViews(APIView):
    """
    View to get the number of casier sold  based on period (week, months, years).
    
    - `Week`: 1, return list of last 7 days with number of casier sold associated.
    - `Months`: 2, return list of last 12 months with number of casier sold associated.
    - `Years`: 3, return list of last 5 years with number of casier sold associated.
    """

    def get_total_casier_sold_by_period(self, periode, product_id=None):
        sales = Vente.objects.filter(is_deleted=False)

        number_casier_sold = []

        if periode == 1:
            start_date = HelperStatictic.get_last_7_days()
            sales = sales.filter(date__gte=start_date)

            for i in range(7):
                day_date = start_date + datetime.timedelta(days=i)
                sales_for_day = sales.filter(date=day_date)
                number_casier = 0

                for sale in sales_for_day:
                    number_casier += self.get_number_casier_sold(sale, product_id)

                number_casier_sold.append({
                    'date': str(day_date),
                    'number_casier': number_casier
                })

        elif periode == 2:
            start_date = HelperStatictic.get_last_12_months()
            for i in range(12):
                month_date = (start_date + relativedelta(months=i)).replace(day=1)
                sales_for_month = sales.filter(date__year=month_date.year, date__month=month_date.month)
                number_casier = 0

                for sale in sales_for_month:
                    number_casier += self.get_number_casier_sold(sale, product_id)

                number_casier_sold.append({
                    'date': f"{month_date.year}-{str(month_date.month).zfill(2)}",
                    'number_casier': number_casier
                })

        elif periode == 3:
            start_date = HelperStatictic.get_last_5_years()
            for i in range(5):
                year_date = start_date.replace(year=start_date.year + i)
                sales_for_year = sales.filter(date__year=year_date.year)
                number_casier = 0

                for sale in sales_for_year:
                    number_casier += self.get_number_casier_sold(sale, product_id)

                number_casier_sold.append({
                    'date': str(year_date.year),
                    'number_casier': number_casier
                })

        return number_casier_sold

    def get_number_casier_sold(self, sale, product_id=None):
        number_casier = 0
        if product_id:
            detail_sale = DetailVente.objects.filter(is_deleted=False, vente=sale, produit=product_id)
        else:
            detail_sale = DetailVente.objects.filter(is_deleted=False, vente=sale)

        for detail in detail_sale:
            number_casier += detail.qte_casier
        
        return number_casier

    def post(self, request):
        periode = int(request.data.get('periode'))
        product_id = request.data.get('product_id', None)
        result = self.get_total_casier_sold_by_period(periode, product_id)
        return Response({"data": result})
   


class StatisticTotalAmountOrderViews(APIView):
    """
    View to get the total amount of orders based on period (week, months, years).
    
    - `Week`: 1, return list of last 7 days with total amount of orders associated.
    - `Months`: 2, return list of last 12 months with total amount of orders associated.
    - `Years`: 3, return list of last 5 years with total amount of orders associated.
    """

    def get_total_amount_orders_by_period(self, periode, product_id=None):
        orders = Commande.objects.filter(is_deleted=False)

        total_amounts = []

        if periode == 1:
            start_date = HelperStatictic.get_last_7_days()
            orders = orders.filter(date__gte=start_date)

            for i in range(7):
                day_date = start_date + datetime.timedelta(days=i)
                orders_for_day = orders.filter(date=day_date)
                total_amount = 0

                for order in orders_for_day:
                    total_amount += self.get_total_amount_for_order(order, product_id)
                    
                

                total_amounts.append({
                    'date': str(day_date),
                    'total_amount': total_amount
                })

        elif periode == 2:
            start_date = HelperStatictic.get_last_12_months()
            for i in range(12):
                month_date = (start_date + relativedelta(months=i)).replace(day=1)
                orders_for_month = orders.filter(date__year=month_date.year, date__month=month_date.month)
                total_amount = 0

                for order in orders_for_month:
                    total_amount += self.get_total_amount_for_order(order, product_id)

                total_amounts.append({
                    'date': f"{month_date.year}-{str(month_date.month).zfill(2)}",
                    'total_amount': total_amount
                })

        elif periode == 3:
            start_date = HelperStatictic.get_last_5_years()
            for i in range(5):
                year_date = start_date.replace(year=start_date.year + i)
                orders_for_year = orders.filter(date__year=year_date.year)
                total_amount = 0

                for order in orders_for_year:
                    total_amount += self.get_total_amount_for_order(order, product_id)

                total_amounts.append({
                    'date': str(year_date.year),
                    'total_amount': total_amount
                })

        return total_amounts

    def get_total_amount_for_order(self, order, product_id=None):
        total_amount = 0
        if product_id:
            detail_order = DetailCommande.objects.filter(is_deleted=False, commande=order, produit=product_id)
        else:
            detail_order = DetailCommande.objects.filter(is_deleted=False, commande=order)

        for detail in detail_order:
            total_amount += Helper.get_total_detail_commande(detail)
        total_amount += int(order.frais_transport)

        return total_amount

    def post(self, request):
        periode = int(request.data.get('periode'))
        product_id = request.data.get('product_id', None)
        result = self.get_total_amount_orders_by_period(periode, product_id)
        return Response({"data": result})

class StatisticNumberOfConsignation(APIView):
    """
    View to get the number of consignments, optionally filtered by client.
    
    - `client_id`: The ID of the client to filter consignments.
    """

    def post(self, request):
        client_id = request.data.get('client_id')
        if client_id:
            number_of_consignation = Consignation.objects.filter(is_deleted=False, client=client_id,type_consignation=1).count()
        else:
            number_of_consignation = Consignation.objects.filter(is_deleted=False,type_consignation=1).count()
        return Response({"number_of_consignation":number_of_consignation})


