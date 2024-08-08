from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from home.models import Company
from .models import Miscellaneous
from selling.models import Selling_payment_history
from labour.models import LabourBill
from raw_materials.models import Material_payment_history


# Create your views here.
@login_required
def accounts(request):
    cprofile = get_object_or_404(Company, id=1)

    debit_data = Selling_payment_history.objects.all().order_by('-issue_date')

    paginator = Paginator(debit_data, 10)  # Number of items per page

    page_number1 = request.GET.get('page')
    try:
        page_data1 = paginator.page(page_number1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data1 = paginator.page(paginator.num_pages)
    
    credit_data1 = LabourBill.objects.all().order_by('-date')
    credit_data2 = Miscellaneous.objects.all().order_by('-date')
    credit_data3 = Material_payment_history.objects.all().order_by('-date')

    combine_credit = list(credit_data1) + list(credit_data2) + list(credit_data3)

    sorted_credit = sorted(combine_credit, key=lambda x: x.date, reverse=True)

    paginator = Paginator(sorted_credit, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    
    queryset = request.GET.get('queryset')
    debit_query = request.GET.get('debit_query')

    queryset_ids = [int(id_str) for id_str in queryset.split(',')] if queryset else []
    debit_query_ids = [int(id_str) for id_str in debit_query.split(',')] if debit_query else []

    combine_queryset = None
    debit_queryset = None
    
    if queryset:
        # If queryset parameter is present, convert it back to queryset object
        queryset0 = LabourBill.objects.filter(id__in=queryset_ids)
        queryset1 = Miscellaneous.objects.filter(id__in=queryset_ids)
        queryset2 = Material_payment_history.objects.filter(id__in=queryset_ids)

        combine_queryset = list(queryset0) + list(queryset1) + list(queryset2)

    
    if debit_query:
        # If queryset parameter is present, convert it back to queryset object
        debit_queryset = Selling_payment_history.objects.filter(id__in=debit_query_ids)


    context = {
        'profile': cprofile,
        'debit_data' : page_data1,
        'combine_queryset' : combine_queryset,
        'debit_queryset' : debit_queryset,
        'sorted_credit' : page_data
    }
    return render(request, 'accounts/accounts.html', context)


@login_required
def search_accounts(request):
    if request.method == 'POST':
        account_date = request.POST['account_date']

        labour_bill_queryset = LabourBill.objects.filter(date__date=account_date)
        miscellaneous_queryset = Miscellaneous.objects.filter(date__date=account_date)
        material_bill_queryset = Material_payment_history.objects.filter(date__date=account_date)

        # Combine the querysets into a single list
        combined_queryset = list(labour_bill_queryset) + list(miscellaneous_queryset) + list(material_bill_queryset)

        # Get a list of IDs from the combined queryset
        ids_list = [item.id for item in combined_queryset]

        debit_queryset = Selling_payment_history.objects.filter(issue_date__date = account_date)

        debit_list = [item.id for item in debit_queryset]
        
        redirect_url = reverse('accounts')
        query_params = {
            'queryset': ",".join(map(str, ids_list)),
            'debit_query': ",".join(map(str, debit_list)),
        }
        redirect_url += '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])

        # Redirect back to the 'accounts' view with query parameters
        return HttpResponseRedirect(redirect_url)
    else:
        # If method is not POST, redirect back to the 'accounts' view without any changes
        return HttpResponseRedirect(reverse('accounts'))


@login_required
def miscelleneous(request):
    cprofile = get_object_or_404(Company, id=1)
    if request.method == 'POST':
        title = request.POST['cost_title']
        amount = request.POST['amount']

        misce = Miscellaneous.objects.create(title = title, amount = amount)
        misce.save()

    miscell = Miscellaneous.objects.all().order_by('-id')
    paginator = Paginator(miscell, 10)  # Number of items per page

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
        queryset = Miscellaneous.objects.filter(id__in=key_value.split(','))

    context = {
        'miscell': page_data,
        'queryset': queryset,
        'profile': cprofile
    }
    return render(request, 'accounts/miscelleneous.html', context)


@login_required
def search_miscllenous(request):
    queryset = Miscellaneous.objects.all()

    if request.method  == 'POST':
        search_issue_date = request.POST['search_miscllenous']
        queryset = queryset.filter(date__date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('miscelleneous') + f'?queryset={",".join(map(str, ids_list))}')