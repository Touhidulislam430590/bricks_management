from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from .models import Selling, Selling_payment_history

from .forms import SellingSearchForm
from home.models import Company


# Create your views here.
@login_required
def selling(request):    
    if request.method == 'POST':
        selling_Type = request.POST['selling_Type']
        bricks_type = request.POST['bricks_type']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        rate = request.POST['rate']
        quantity = request.POST['quantity']
        total_price = request.POST['total_price']
        payment = request.POST['payment']
        due = request.POST['due']
        commission = request.POST['commission']
        
        # print(selling_Type, bricks_type, name, phone, address, rate, quantity, total_price, payment, due, commission)

        sell = Selling.objects.create(selling_type = selling_Type, Bricks_type = bricks_type, customer_name = name, customer_address = address, customer_mobile = phone, product_rate = rate, product_quantity = quantity, total_price = total_price, payment = payment, commission = commission, due = due)
        sell.save()
        sell_history = Selling_payment_history.objects.create(customer_name = name, amount = payment)
        sell_history.save()

        return redirect('selling')

    
    all_sell = Selling.objects.filter(is_pending = False).order_by('-id')
    paginator = Paginator(all_sell, 10)  # Number of items per page

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_data = paginator.page(paginator.num_pages)

    cprofile = get_object_or_404(Company, id=1)

    key_value = request.GET.get('queryset')
    queryset = None
    
    if key_value:
        # If queryset parameter is present, convert it back to queryset object
        queryset = Selling.objects.filter(id__in=key_value.split(','))

    

    context = {
        'all_sell' : page_data,
        'queryset' : queryset,
        'profile': cprofile
    }

    return render(request, 'selling/selling.html', context)


@login_required
def search_selling(request):
    
    queryset = Selling.objects.all()

    if request.method  == 'POST':
        search_issue_date = request.POST['search_selling']
        queryset = queryset.filter(issue_date__date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('selling') + f'?queryset={",".join(map(str, ids_list))}')


@login_required
def sellInfo(request, id):
    cprofile = get_object_or_404(Company, id=1)
    sell_info = Selling.objects.get(id = id, is_pending = False)

    context = {
        'sell_info' : sell_info,
        'profile': cprofile
    }

    return render(request, 'selling/selling_info.html', context)


@login_required
def due_payment(request):
    cprofile = get_object_or_404(Company, id=1)
    due_info = Selling.objects.filter(due__gt = 0).order_by('-id')

    paginator = Paginator(due_info, 10)  # Number of items per page

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
        due_queryset = Selling.objects.filter(id__in=key_value1.split(','))
    
    context = {
        'due_info' : page_data,
        'due_queryset' : due_queryset,
        'profile': cprofile
    }

    return render(request, 'selling/due_payment.html', context)


@login_required
def due_search_selling(request):
    
    queryset = Selling.objects.filter(due__gt = 0).order_by('-id')

    if request.method  == 'POST':
        search_issue_date = request.POST['search_selling']
        queryset = queryset.filter(issue_date__date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('due_list') + f'?queryset={",".join(map(str, ids_list))}')


@login_required
def sell_print(request, id):
    cprofile = get_object_or_404(Company, id=1)

    sell_info = Selling.objects.get(id = id)

    context = {
        'profile' : cprofile,
        'sell_info' : sell_info
    }
    return render(request, 'selling/sell_invoice.html', context)


@login_required
def due_form(request, id):
    cprofile = get_object_or_404(Company, id=1)
    due_info = Selling.objects.get(id = id)


    if request.method == 'POST':
        pay = request.POST['payment']

        if int(due_info.due) >= int(pay):
            previous_due = due_info.due

            due_info.due = int(due_info.due) - int(pay)
            sell_history = Selling_payment_history.objects.create(customer_name = due_info.customer_name, amount = pay)
            sell_history.save()
            due_info.save()


            redirect_url = reverse('due_invoice', kwargs={'id': id})
            redirect_url += f'?pay={pay}&previous_due={previous_due}'
            return redirect(redirect_url)

    context = {
        'profile' : cprofile,
        'due_info' : due_info
    }
    return render(request, 'selling/due_form.html', context)


@login_required
def due_invoice(request, id):
    cprofile = get_object_or_404(Company, id=1)
    due_invoice = Selling.objects.get(id = id)

    pay = request.GET.get('pay')
    previous_due = request.GET.get('previous_due')


    context = {
        'profile' : cprofile,
        'due_invoice' : due_invoice,
        'previous_due' : previous_due,
        'pay' : pay
    }
    return render(request, 'selling/due_selling_invoice.html', context)



def payment_history(request):
    cprofile = get_object_or_404(Company, id=1)
    hist = Selling_payment_history.objects.all().order_by('-id')

    context = {
        'hist' : hist,
        'profile' : cprofile,
    }
    return render(request, 'selling/payment_history.html', context)
