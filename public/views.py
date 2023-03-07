from django.shortcuts import render

# Create your views here.

def index (request):
    context = {}
    return render(request, 'public/index.html', context)

def about (request):
    context = {}
    return render(request, 'public/about.html', context)

def contact (request):
    context = {}
    context['email'] = "gcoinsbank@gmail.com"
    
    return render(request, 'public/contact.html', context)

    