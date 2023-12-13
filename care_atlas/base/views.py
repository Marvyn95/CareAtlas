from django.shortcuts import render
import datetime

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_page(request):
    date_1 = datetime.datetime.now().date()
    print(date_1)
    return render(request, 'base/application_page.html')