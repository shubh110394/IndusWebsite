from distutils.log import error
from django.shortcuts import render
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer


# Create your views here.

def index(request):
    products = Product.get_all_products()
    categories = Category.get_all_categories()

    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request,'index.html',data)
    # return render(request,'orders/order.html')


def signup(request):
    if(request.method == "GET"):
        return render(request,'signup.html')
    else:
        postData = request.POST
        first_name = postData.get("firstname")
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        #validation
        error_message = None

        if(not first_name):
            error_message = "First name required"
        elif len(first_name)< 4:
            error_message = "First name should be atleast 4 in length"
        elif not last_name:
            error_message = "Last Name required"
        elif len(last_name)<4:
            error_message = "Last name should be atleast 4 in length"
        elif not phone:
            error_message = "Phone number is required"
        elif len(phone) < 10:
            error_message = "Phone number must be 10 character long"
        elif len(password) < 6:
            error_message = "Password must be 6 character long"
        elif len(email) < 5:
            error_message = "Email must be 5 character long"


                

        #saving
        if not error_message:
            # print(first_name,last_name,password)
            customer = Customer(first_name = first_name,last_name = last_name,phone = phone,email = email,password = password)
            customer.register()
        else:
            return render(request,'signup.html',{"error":error_message})
        return HttpResponse("signup Success")
