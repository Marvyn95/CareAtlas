from django.shortcuts import render

# Create your views here.
def home_page(request):
    context = {}
    return render(request, 'base/home_page.html', context)