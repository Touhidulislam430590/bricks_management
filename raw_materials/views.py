from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from home.models import Company
from .models import Soil, Petroleum, Material_payment_history


# Create your views here.
@login_required
def raw_materials(request):
    cprofile = get_object_or_404(Company, id=1)
    soil_data = Soil.objects.all()
    petroleum_data = Petroleum.objects.all()

    combined_data = list(petroleum_data) + list(soil_data)
    
    # Sort the combined data by issue_date
    sorted_combined_data = sorted(
        combined_data,
        key=lambda x: x.issue_date,
        reverse=True
    )

    paginator = Paginator(sorted_combined_data, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    key_value = request.GET.get('queryset')
    combine_queryset = None
    
    if key_value:
        # If queryset parameter is present, convert it back to queryset object
        queryset = Soil.objects.filter(id__in=key_value.split(','))
        queryset1 = Petroleum.objects.filter(id__in=key_value.split(','))

        combine_queryset = list(queryset) + list(queryset1)

    context = {
        'combine_data' : page_data,
        'combine_queryset' : combine_queryset,
        'profile' : cprofile,
    }
    return render(request, 'raw_materials/raw_materials.html', context)


@login_required
def search_raw_materials(request):
    if request.method == 'POST':
        search_issue_date = request.POST.get('search_raw_materials')
        
        # Perform search in both Soil and Petroleum models
        soil_queryset = Soil.objects.filter(issue_date__date=search_issue_date)
        petroleum_queryset = Petroleum.objects.filter(issue_date__date=search_issue_date)

        # Combine the querysets into a single list
        combined_queryset = list(soil_queryset) + list(petroleum_queryset)

        # Get a list of IDs from the combined queryset
        ids_list = [item.id for item in combined_queryset]

        # Redirect back to the raw_materials view with the list of IDs as a query parameter
        return HttpResponseRedirect(reverse('raw_materials') + f'?queryset={",".join(map(str, ids_list))}')
    else:
        # If method is not POST, redirect back to the raw_materials view without any changes
        return HttpResponseRedirect(reverse('raw_materials'))


@login_required
def petroleum(request):
    if request.method == 'POST':
        petroleum_Type = request.POST['petroleum_Type']
        vendor_name2 = request.POST['vendor_name2']
        quantity2 = request.POST['quantity2']
        rate2 = request.POST['rate2']
        payment2 = request.POST['payment2']

        total_price = float(rate2) * float(quantity2)
        due = total_price - float(payment2)

        petroleum_info = Petroleum.objects.create(petroleum_type = petroleum_Type, vendor_name = vendor_name2, quantity = quantity2, rate = rate2, total_price = total_price, done_payment = payment2, due = due)
        petroleum_info.save()

    return redirect('raw_materials')


@login_required
def soil(request):
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        sarder_name = request.POST['sarder_name']
        rate = request.POST['rate']
        quantity = request.POST['quantity']
        payment = request.POST['payment']

        total_price = float(rate) * float(quantity)
        due = total_price - float(payment)

        soil_info = Soil.objects.create(vendor_name = vendor_name, quantity = quantity, rate = rate, total_price = total_price, sarder_name = sarder_name, done_payment = payment, due = due)
        soil_info.save()


    return redirect('raw_materials')


@login_required
def due_materials(request):
    cprofile = get_object_or_404(Company, id=1)
    soil_data = Soil.objects.filter(due__gt = 0)
    petroleum_data = Petroleum.objects.filter(due__gt = 0)

    combined_data = list(petroleum_data) + list(soil_data)
    
    # Sort the combined data by issue_date
    sorted_combined_data = sorted(
        combined_data,
        key=lambda x: x.issue_date,
        reverse=True
    )

    paginator = Paginator(sorted_combined_data, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    context = {
        'combine_data' : page_data,
        'profile' : cprofile,
    }
    return render(request, 'raw_materials/due_materials.html', context)


@login_required
def due_details(request, id, vendor_name):
    cprofile = get_object_or_404(Company, id=1)
    soil_data = Soil.objects.filter(id=id, vendor_name=vendor_name).first()

    # If not found in Soil table, check in Petroleum table
    if soil_data is None:
        petroleum_data = Petroleum.objects.filter(id=id, vendor_name=vendor_name).first()
        if petroleum_data:
            data = petroleum_data
            data_type = 'petroleum'
        else:
            # Handle the case where data with the given ID and vendor name is not found
            raise Http404("Data not found")
    else:
        data = soil_data
        data_type = 'soil'

    context = {
        'data': data,
        'data_type': data_type,
        'profile' : cprofile,
    }
    return render(request, 'raw_materials/due_details.html', context)


@login_required
def due_invoice(request, id, data_type):
    cprofile = get_object_or_404(Company, id=1)
    if request.method == 'POST':
        amount = request.POST['amount']
        
        if data_type == 'soil':
            data = Soil.objects.get(id = id)
        elif data_type == 'petroleum':
            data = Petroleum.objects.get(id = id)

        if int(data.due) >= int(amount):
            previous_due = data.due
            data.done_payment += float(amount)
            data.due = float(data.total_price) - float(data.done_payment)
            data.save()

            hist_data = Material_payment_history.objects.create(vendor_name = data.vendor_name, amount = amount)
            hist_data.save()
                        
        

    context = {
        'profile' : cprofile,
        'data' : data,
        'previous_due' : previous_due
    }
    return render(request, 'raw_materials/due_invoice.html', context)


@login_required
def material_payment_history(request):
    cprofile = get_object_or_404(Company, id=1)
    paid_bills = Material_payment_history.objects.all()

    paginator = Paginator(paid_bills, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)


    context = {
            'profile' : cprofile,
            'paid_bills' : page_data
        }
    return render(request, 'raw_materials/materials_payment_list.html', context)