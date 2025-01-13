from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'Home.html')

def about(request):
    return render(request, 'About.html')

def careers(request):
    return render(request, 'Careers.html')