from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Daily_Production
from labour.models import LabourDeal  # Check the import path here
from home.models import Company


@login_required
def production(request):
    cprofile = get_object_or_404(Company, id=1)
    labour_info = LabourDeal.objects.all()

    if request.method == 'POST':
        labour_instance = request.POST['labour_instance']
        production = request.POST['production']
        description = request.POST['description']

        labour_data = LabourDeal.objects.get(id = labour_instance)

        labour_data.complete_production += int(production)

        if labour_data.payment_sequence == 'production':
            production_bill = float(production) * float(labour_data.rate)
            due_bill = production_bill
        else:
            production_bill = 0
            due_bill = production_bill

        data = Daily_Production.objects.create(labour_instance = labour_data, production = production, description = description, total_bill = production_bill, paid_bill = 0, due_bill = due_bill)
        data.save()
        labour_data.save()

    production_data = Daily_Production.objects.all().order_by('-id')
    paginator = Paginator(production_data, 10)  # Number of items per page

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

    context = {
        'labour': labour_info,
        'profile': cprofile,
        'queryset': queryset,
        'production_data' : page_data
    }
    return render(request, 'production/production.html', context)


@login_required
def search_production(request):
    
    queryset = Daily_Production.objects.all()

    if request.method  == 'POST':
        search_issue_date = request.POST['search_production']
        queryset = queryset.filter(issue_date=search_issue_date)


    # Get a list of IDs from the filtered queryset
    ids_list = list(queryset.values_list('id', flat=True))

    # Redirect back to the selling view with the list of IDs as a query parameter
    return HttpResponseRedirect(reverse('production') + f'?queryset={",".join(map(str, ids_list))}')


