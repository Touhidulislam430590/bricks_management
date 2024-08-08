from django import forms

class SellingSearchForm(forms.Form):
    search_id = forms.IntegerField(label='Search by ID', required=False)
    search_issue_date = forms.DateTimeField(label='Search by Issue Date', required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
