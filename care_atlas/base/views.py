from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_page(request):
    return render(request, 'base/application_page.html')