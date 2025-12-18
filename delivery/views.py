from django.http import HttpResponse
from django.shortcuts import render

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
        return HttpResponse("Signup Successfull")
    else:
        return HttpResponse("Signup unsuccessfull")