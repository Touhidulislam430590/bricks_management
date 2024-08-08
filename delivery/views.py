from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from datetime import datetime

from home.models import Company
from selling.models import Selling
from .models import Delivery, Delivery_History


# Create your views here.
@login_required
def delivery(request):
    
    cprofile = get_object_or_404(Company, id=1)

    # Retrieve the queryset parameter from the URL
    queryset_param = request.GET.get('queryset')
    
    if queryset_param:
        # Split the queryset parameter to extract IDs
        ids_list = queryset_param.split(',')
        # Filter delivery_data based on IDs from the queryset
        delivery_data = Delivery.objects.filter(id__in=ids_list)
    else:
        # If no queryset parameter, retrieve all data as before
        delivery_data = Delivery.objects.filter(pending_delivery__gt=0)

    # Pagination logic
    paginator = Paginator(delivery_data, 10)  # Number of items per page
    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    data = {
        'profile': cprofile,
        'delivery': page_data
    }
    return render(request, 'delivery/delivery.html', data)


@login_required
def delivery_search(request):

    if request.method == 'GET':
        search_id = request.GET.get('search_id')
        if search_id:
            # Perform the search based on the ID
            delivery_data = Delivery.objects.filter(selling_id=search_id)
        else:
            # If no search ID provided, redirect back to the main delivery view
            return HttpResponseRedirect(reverse('delivery'))

    # Check if delivery_data is defined (after the search)
    if 'delivery_data' in locals():
        ids_list = list(delivery_data.values_list('id', flat=True))
        # Redirect back to the delivery view with the list of IDs as a query parameter
        return HttpResponseRedirect(reverse('delivery') + f'?queryset={",".join(map(str, ids_list))}')
    else:
        # If delivery_data is not defined (no search performed), redirect without query parameter
        return HttpResponseRedirect(reverse('delivery'))


def ready_to_delivery(request, id):
    data = Selling.objects.get(id = id)
    data.is_pending = True

    selling_id = data.id
    customer_name = data.customer_name
    customer_address = data.customer_address
    customer_mobile = data.customer_mobile
    product_quantity = data.product_quantity
    pending_delivery = data.product_quantity

    delivery_data = Delivery.objects.create(selling_id = selling_id, customer_name = customer_name, customer_address = customer_address, customer_mobile = customer_mobile, product_quantity = product_quantity, pending_delivery = pending_delivery)

    delivery_data.save()
    data.save()

    # print(data.is_pending)
    return redirect('delivery')


@login_required
def delivery_info(request, id):
    cprofile = get_object_or_404(Company, id=1)
    delivery_instance = get_object_or_404(Delivery, id=id)

    if request.method == 'POST':
        delivery_amount = request.POST.get('delivery_amount')
        driver_name = request.POST.get('driver_name')

        if delivery_amount and delivery_instance.pending_delivery > 0:
            delivery_amount = int(delivery_amount)
            if delivery_amount <= delivery_instance.pending_delivery:
                delivery_instance.pending_delivery -= delivery_amount
                delivery_instance.delivered += delivery_amount
                delivery_instance.save()

                Delivery_History.objects.create(delivery=delivery_instance, delivery_amount=delivery_amount, driver_name = driver_name)
                # Delivery_History.save()
                redirect_url = reverse('delivery_challan', kwargs={'id': id})
                redirect_url += f'?delivery_amount={delivery_amount}&pending_delivery={delivery_instance.pending_delivery}&driver_name={driver_name}&created={Delivery_History.created}'
                return redirect(redirect_url)

    context = {
        'delivery': delivery_instance,
        'profile': cprofile
    }
    return render(request, 'delivery/delivery_details.html', context)


@login_required
def delivery_done(request):
    cprofile = get_object_or_404(Company, id=1)

    # Retrieve the queryset parameter from the URL
    queryset_param = request.GET.get('queryset')
    
    if queryset_param:
        # Split the queryset parameter to extract IDs
        ids_list = queryset_param.split(',')
        # Filter delivery_data based on IDs from the queryset
        delivery_data = Delivery.objects.filter(id__in=ids_list)
    else:
        # If no queryset parameter, retrieve all data as before
        delivery_data = Delivery.objects.filter(pending_delivery = 0).order_by('-id')



    paginator = Paginator(delivery_data, 10)  # Number of items per page

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
        "delivery_done" : page_data,
        'delivery_data' : delivery_data,
        'profile': cprofile
    }
    return render(request, 'delivery/delivery_done.html', context)


@login_required
def delivery_done_search(request):
    if request.method == 'GET':
        search_id = request.GET.get('search_id')
        if search_id:
            # Perform the search based on the ID
            delivery_data = Delivery.objects.filter(selling_id=search_id)
        else:
            # If no search ID provided, redirect back to the main delivery view
            return HttpResponseRedirect(reverse('delivery_done'))

    # Check if delivery_data is defined (after the search)
    if 'delivery_data' in locals():
        ids_list = list(delivery_data.values_list('id', flat=True))
        # Redirect back to the delivery view with the list of IDs as a query parameter
        return HttpResponseRedirect(reverse('delivery_done') + f'?queryset={",".join(map(str, ids_list))}')
    else:
        # If delivery_data is not defined (no search performed), redirect without query parameter
        return HttpResponseRedirect(reverse('delivery_done'))


@login_required
def delivery_report(request):
    cprofile = get_object_or_404(Company, id=1)
    all_history = Delivery_History.objects.all().order_by('-id')

    paginator = Paginator(all_history, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    key_value1 = request.GET.get('queryset')

    due_queryset = None
    
    if key_value1:
        # If queryset parameter is present, convert it back to queryset object
        due_queryset = Delivery_History.objects.filter(id__in=key_value1.split(','))

    print(due_queryset)

    context = {
        'all_history' : page_data,
        'due_queryset' : due_queryset,
        'profile': cprofile
    }
    return render(request, 'delivery/delivery_history.html', context)


@login_required
def search_delivery_history(request):
    queryset = Delivery_History.objects.all().order_by('-id')

    if request.method  == 'POST':
        search_issue_date = request.POST['search_selling']
        queryset = queryset.filter(created__date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('delivery_report') + f'?queryset={",".join(map(str, ids_list))}')


@login_required
def delivery_challan(request, id):
    cprofile = get_object_or_404(Company, id=1)

    delivery = Delivery.objects.get(id = id)

    delivery_amount = request.GET.get('delivery_amount')
    pending_delivery = request.GET.get('pending_delivery')
    driver_name = request.GET.get('driver_name')

    delivery_time = datetime.now()

    # print(delivery.delivery.customer_mobile)

    context = {
        'profile' : cprofile,
        'delivery_amount' : delivery_amount,
        'pending_delivery' : pending_delivery,
        'driver_name' : driver_name,
        'delivery_time' : delivery_time,
        'delivery' : delivery
    }
    return render(request, 'delivery/delivery_challan.html', context)