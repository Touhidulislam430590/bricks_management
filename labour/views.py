from django.db import OperationalError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from home.models import Company
from production.models import Daily_Production
from .models import LabourBill, LabourDeal, LabourType


# Create your views here.
@login_required
def labours(request):
    cprofile = get_object_or_404(Company, id=1)
    deals = LabourDeal.objects.all().order_by('-id')

    paginator = Paginator(deals, 10)  # Number of items per page

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
        'deals' : page_data,
        'profile': cprofile
    }
    return render(request, 'labour/labour.html', context)


@login_required
def new_deal(request):
    if request.method == 'POST':
        # Assuming you have a form defined using Django forms, you can access the data using request.POST
        labour_type_id = request.POST.get('labour_type')
        sarder_name = request.POST.get('sarder_name')
        payment_sequence = request.POST.get('payment_sequence')
        rate = request.POST.get('rate')
        requirements = request.POST.get('requirements')
        number_of_employee = request.POST.get('number_of_employee')
        starting_date = request.POST.get('starting_date')
        closing_date = request.POST.get('closing_date')
        season_target = request.POST.get('season_target')

        labour_type = LabourType.objects.get(id=labour_type_id)

        labour_deal = LabourDeal.objects.create(labour_type = labour_type, sarder_name = sarder_name, payment_sequence=payment_sequence, rate=rate, requirements=requirements, number_of_employee=number_of_employee, starting_date=starting_date, closing_date=closing_date, season_target=season_target)
        labour_deal.save()

        return redirect('labours')
    
    cprofile = get_object_or_404(Company, id=1)

    return render(request, 'labour/new_deal.html', {'labour_types': LabourType.objects.all(), 'profile': cprofile})


@login_required
def add_type(request):
    if request.method == 'POST':
        title = request.POST['title']

        labour_type = LabourType.objects.create(title = title)
        labour_type.save()
        return redirect('labours')
    
    cprofile = get_object_or_404(Company, id=1)
    labours_type = LabourType.objects.all().order_by('-id')
    paginator = Paginator(labours_type, 10)  # Number of items per page

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
        'labour_type' : page_data
    }
    return render(request, 'labour/add_labour_type.html', context)


@login_required
def due_labour(request):
    cprofile = get_object_or_404(Company, id=1)

    due_bills = Daily_Production.objects.filter(due_bill__gt = 0).order_by('-id')

    paginator = Paginator(due_bills, 10)  # Number of items per page

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
    queryset = None
    
    if key_value:
        # If queryset parameter is present, convert it back to queryset object
        queryset = Daily_Production.objects.filter(id__in=key_value.split(','))


    context={
        'profile' : cprofile,
        'queryset' : queryset,
        'due_bills' : page_data
    }
    return render(request, 'labour/due_labour.html', context)


@login_required
def due_labour_search(request):
    queryset = Daily_Production.objects.all()

    if request.method  == 'POST':
        search_issue_date = request.POST['due_labour_search']
        queryset = queryset.filter(issue_date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('due_labour') + f'?queryset={",".join(map(str, ids_list))}')
    

    
@login_required
def due_labour_details(request, id):
    cprofile = get_object_or_404(Company, id=1)
    
    bill_info = Daily_Production.objects.get(id = id)

    context = {
        'profile' : cprofile,
        'bill_info' : bill_info        
    }
    return render(request, 'labour/due_labour_details.html', context)


@login_required
def labour_bill_invoice(request, id):
    cprofile = get_object_or_404(Company, id=1)
    bill_info = Daily_Production.objects.get(id = id)
    if request.method == 'POST':
        payment = request.POST['payment']

        if float(payment) <= bill_info.due_bill:
            pending_bill = bill_info.due_bill

            bill_info.due_bill -= float(payment)
            bill_info.paid_bill += float(payment)

            labour_info = LabourDeal.objects.get(id = bill_info.labour_instance.id)
            bill_history = LabourBill.objects.create(labour_deal = labour_info, bill_amount = payment)
            
            bill_history.save()
            bill_info.save()

            invoice_history = LabourBill.objects.get(id = bill_history.id)

            context = {
                'profile' : cprofile,
                'pending_bill' : pending_bill,
                'labour_info' : labour_info,
                'invoice_history' : invoice_history,
                'bill_info' : bill_info,

            }
            return render(request, 'labour/labour_bill_invoice.html', context)

        else:
            messages.error(request, "Your payment amount is wrong! Please try again.")
            redirect_url = reverse('due_labour_details', kwargs={'id': id})
            return redirect(redirect_url)
    return render(request, 'labour/labour_bill_invoice.html')


@login_required
def labour_bill_history(request):
    cprofile = get_object_or_404(Company, id=1)
    payment_list = LabourBill.objects.all().order_by('-id')

    # Pagination
    paginator = Paginator(payment_list, 10)
    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        page_data = paginator.page(1)
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)

    key_value = request.GET.get('queryset')
    queryset = None
    
    if key_value:
        # If queryset parameter is present, convert it back to queryset object
        queryset = Daily_Production.objects.filter(id__in=key_value.split(','))

    print(queryset)

    context = {
        'payment_list': payment_list,
        'profile': cprofile,
        'queryset': queryset,
        'page_data': page_data
    }
    return render(request, 'labour/labour_history.html', context)


@login_required
def history_search(request):

    if request.method  == 'POST':
        search_id = request.POST['search_by_id']
        queryset_by_id = LabourBill.objects.filter(date__date=search_id)

    ids_query = list(queryset_by_id.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('labour_bill_history') + f'?queryset={",".join(map(str, ids_query))}')


@login_required
def complete_bills(request):
    cprofile = get_object_or_404(Company, id=1)

    paid_bills = Daily_Production.objects.filter(due_bill = 0).order_by('-id')

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

    context={
        'profile' : cprofile,
        'paid_bills' : page_data
    }
    return render(request, 'labour/complete_bills.html', context)