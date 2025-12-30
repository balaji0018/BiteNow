from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import razorpay


from .models import Restaurant, customers, Item, Cart



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
            restaurantList = Restaurant.objects.all()
            return render(request, 'customer_home.html',{"restaurantList" : restaurantList, "username" : username})


    except customers.DoesNotExist:
        return render(request, 'fail.html')
    
def open_add_restaurant(request):
    return render(request, 'add_restaurants.html')


def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
            
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
        return HttpResponse("Successfully Added !")
        #return render(request, 'admin_home.html') open_show_restaurant


def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render (request, 'show_restaurants.html', {"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
        return redirect('open_show_restaurant')  # ✅ URL name
    return render(request, 'admin_home.html')


def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request,"update_restaurant.html", {"restaurant": restaurant})




def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating


        restaurant.save()


    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})


def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)

    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})


def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant, 
                     "username":username})

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = customers.objects.get(username = username)
    cart, created = Cart.objects.get_or_create(customers = customer)
    cart.items.add(item)
    return HttpResponse('added to cart')

def show_cart(request, username):
    customer = customers.objects.get(username = username)
    cart = Cart.objects.filter(customers = customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})


def checkout(request,username):
    customer = get_object_or_404(customers, username = username)
    cart = Cart.objects.filter(customers = customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'error' : 'Your cart is empty',
        })
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })
    


