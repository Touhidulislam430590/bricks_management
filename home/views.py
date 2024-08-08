from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password

from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from openpyxl import Workbook


from .models import Company
from selling.models import Selling_payment_history, Selling
from raw_materials.models import Petroleum, Soil
from labour.models import LabourBill, LabourDeal
from delivery.models import Delivery, Delivery_History
from raw_materials.models import Material_payment_history
from accounts.models import Miscellaneous
from production.models import Daily_Production

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    cprofile = get_object_or_404(Company, id=1)

    last_month_report = get_last_month_data()

    total_sales_last_month = last_month_report['total_sales_last_month']
    total_delivery_last_month = last_month_report['total_delivery_last_month']
    total_labour_bill_last_month = last_month_report['total_labour_bill_last_month']
    total_material_bill_last_month = last_month_report['total_material_bill_last_month']
    last_month_cost = last_month_report['last_month_cost']

    last_week_report = last_week_data()

    last_week_sell = last_week_report['selling_amount']
    last_week_delivery = last_week_report['delivered']
    last_week_labour_bill = last_week_report['labour_bill_amount']
    last_week_material_bill = last_week_report['materials_amount']
    last_week_cost = last_week_report['last_week_cost']

    data = {
        'profile': cprofile,
        'total_sales_last_month': total_sales_last_month,
        'total_delivery_last_month': total_delivery_last_month,
        'total_labour_bill_last_month': total_labour_bill_last_month,
        'total_material_bill_last_month': total_material_bill_last_month,
        'last_month_cost': last_month_cost,

        'last_week_sell': last_week_sell,
        'last_week_delivery': last_week_delivery,
        'last_week_labour_bill': last_week_labour_bill,
        'last_week_material_bill': last_week_material_bill,
        'last_week_cost': last_week_cost,
    }
    return render(request, 'home/home.html', data)


@login_required
def company(request):
    cprofile = get_object_or_404(Company, id=1)

    if request.method == 'POST':
        name = request.POST['c_name']
        mobile = request.POST['c_mobile']
        address = request.POST['c_address']
        
        cprofile.cname = name
        cprofile.cmobile = mobile
        cprofile.caddress = address

        cprofile.save()


    data = {
        'profile': cprofile
    }
    return render(request, 'home/company_profile.html', data)


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'home/login.html', {'error_message': error_message})
    return render(request, 'home/login.html')




def get_last_month_data():
    # Get the current date
    current_date = datetime.now()

    # Calculate the first day of the current month
    first_day_current_month = current_date.replace(day=1)

    # Calculate the last day of the previous month
    last_day_previous_month = first_day_current_month - timedelta(days=1)

    # Calculate the first day of the previous month
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Filter sales data for the previous month
    last_month_sales = Selling_payment_history.objects.filter(issue_date__range=[first_day_previous_month, last_day_previous_month])
    total_sales_last_month = last_month_sales.aggregate(amount=Sum('amount'))['amount'] or 0
    
    # Filter Labour Bill data for the previous month
    last_month_labour_bill = LabourBill.objects.filter(date__range=[first_day_previous_month, last_day_previous_month])
    total_labour_bill_last_month = last_month_labour_bill.aggregate(bill_amount=Sum('bill_amount'))['bill_amount'] or 0
    
    # Filter Delivery data for the previous month
    last_month_delivery_amount = Delivery_History.objects.filter(created__range=[first_day_previous_month, last_day_previous_month])
    total_delivery_last_month = last_month_delivery_amount.aggregate(delivery_amount=Sum('delivery_amount'))['delivery_amount'] or 0
    
    # Filter Delivery data for the previous month
    last_month_materials_bill_amount = Material_payment_history.objects.filter(date__range=[first_day_previous_month, last_day_previous_month])
    total_material_bill_last_month = last_month_materials_bill_amount.aggregate(amount=Sum('amount'))['amount'] or 0
    
    # Filter Miscellaneous data for the previous month
    last_month_miscellaneous_amount = Miscellaneous.objects.filter(date__range=[first_day_previous_month, last_day_previous_month])
    total_miscellaneous_last_month = last_month_miscellaneous_amount.aggregate(amount=Sum('amount'))['amount'] or 0

    last_month_cost = total_labour_bill_last_month + total_material_bill_last_month + total_miscellaneous_last_month

    last_month_report = {
        'total_sales_last_month' : total_sales_last_month,
        'total_labour_bill_last_month' : total_labour_bill_last_month,
        'total_delivery_last_month' : total_delivery_last_month,
        'total_material_bill_last_month' : total_material_bill_last_month,
        'last_month_cost' : last_month_cost,
    }

    return last_month_report



def last_week_data():
    # Calculate the date 7 days ago from today
    seven_days_ago_aware = timezone.now() - timedelta(days=7)

    # Convert the timezone-aware datetime to naive datetime
    seven_days_ago_naive = seven_days_ago_aware.replace(tzinfo=None)

    # Make sure seven_days_ago is timezone-aware
    seven_days_ago = timezone.make_aware(seven_days_ago_naive)

    print(seven_days_ago)

    # Calculate the sales amount for the last 7 days issue_date
    last_7_days_sales = Selling_payment_history.objects.filter(issue_date__gte=seven_days_ago).aggregate(amount=Sum('amount'))
    # If there are no sales in the last 7 days, set the amount to 0
    selling_amount = last_7_days_sales['amount'] or 0

    # Calculate the sales amount for the last 7 days issue_date
    last_week_delivery = Delivery_History.objects.filter(created__date__gte=seven_days_ago).aggregate(delivery_amount=Sum('delivery_amount'))
    # If there are no sales in the last 7 days, set the amount to 0
    delivered = last_week_delivery['delivery_amount'] or 0

    # Calculate the sales amount for the last 7 days issue_date
    last_week_labour_bill = LabourBill.objects.filter(date__date__gte=seven_days_ago).aggregate(bill_amount=Sum('bill_amount'))
    # If there are no sales in the last 7 days, set the amount to 0
    labour_bill_amount = last_week_labour_bill['bill_amount'] or 0

    # Calculate the sales amount for the last 7 days issue_date
    last_week_materials_payment = Material_payment_history.objects.filter(date__date__gte=seven_days_ago).aggregate(amount=Sum('amount'))
    # If there are no sales in the last 7 days, set the amount to 0
    materials_amount = last_week_materials_payment['amount'] or 0

    # Calculate the sales amount for the last 7 days issue_date
    last_week_miscellaneous = Miscellaneous.objects.filter(date__date__gte=seven_days_ago).aggregate(amount=Sum('amount'))
    # If there are no sales in the last 7 days, set the amount to 0
    miscellaneous_amount = last_week_miscellaneous['amount'] or 0

    last_week_cost = miscellaneous_amount + labour_bill_amount + materials_amount

    last_week_report = {
        'selling_amount' : selling_amount,
        'delivered' : delivered,
        'labour_bill_amount' : labour_bill_amount,
        'materials_amount' : materials_amount,
        'last_week_cost' : last_week_cost,
    }

    return last_week_report


@login_required
def new_season(request):
    # if not request.session.get('password_verified'):
    #     return redirect('password_required_form')
    cprofile = get_object_or_404(Company, id=1)
    
    data = {
        'profile': cprofile
    }
    return render(request, 'home/new_season.html', data)


@login_required
def password_required_form(request):
    cprofile = get_object_or_404(Company, id=1)
    data = {
        'profile': cprofile
    }
    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if check_password(entered_password, request.user.password):
            return download_and_delete_data()  # Return the HttpResponse directly
        else:
            return render(request, 'home/password_required_form.html', {'error': 'Incorrect password', 'profile': cprofile})
        
    
    return render(request, 'home/password_required_form.html', data)



from django.db.models import Q

def download_and_delete_data():
    models = [Selling_payment_history, Delivery_History, Delivery, LabourDeal, LabourBill, Daily_Production, Material_payment_history, Miscellaneous, Selling, Petroleum, Soil]

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="all_models.xlsx"'

    wb = Workbook()
    wb.remove(wb.active)  # Remove the default sheet created by openpyxl

    for model in models:
        ws = wb.create_sheet(title=model._meta.verbose_name)
        fields = [field.name for field in model._meta.fields]
        
        # Write the header
        ws.append(fields)
        
        # Initialize an empty queryset
        queryset = model.objects.none()

        # Apply specific filters based on model type
        if model == Selling:
            queryset = model.objects.filter(Q(is_delivered=True) | Q(selling_type='Instant Selling'))
        
        if model in [Petroleum, Soil]:
            queryset |= model.objects.filter(due=0)
        
        if model == Delivery:
            queryset |= model.objects.filter(pending_delivery=0)  # No deletion condition, just a placeholder

        if model not in [Selling, Petroleum, Soil, Delivery_History]:
            queryset |= model.objects.all()

        for obj in queryset:
            try:
                row = [str(getattr(obj, field)) for field in fields]  # Convert data to string
                ws.append(row)
            except Exception as e:
                print(f"Error exporting data: {e}")
        
        # Delete data after exporting
        queryset.delete()
    
    wb.save(response)
    
    return response