from django.http import HttpResponse
from django.shortcuts import render
from .models import customers



# Create your views here.
def hello(request):
    return render(request, "index.html")


def open_signup(request):
    return render(request, "signup.html")

def open_signin(request):
    return render(request, "signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        if customers.objects.filter(email = email).exists():
            return HttpResponse("This email is already registered. Please use another email_id.")


        customers_data = customers(username = username, password = password, email = email, mobile = mobile, address= address)
        customers_data.save()
        return render(request, "signin.html") 
        #return HttpResponse("Signup Successfull")
    else:
        return HttpResponse("Signup unsuccessfull")
    
        
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


    try:
        customers.objects.get(username = username, password = password)
        if username == 'admin':
            return render(request, 'admin_home.html')
        else:
            return render(request, 'customer_home.html')


    except customers.DoesNotExist:
        return render(request, 'fail.html')