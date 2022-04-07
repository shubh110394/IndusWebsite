from distutils.log import error
import email
from wsgiref import validate
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View


# Create your views here.

class Index(View):
    def get(self, request):
        # request.session.get("cart").clear()
        products = Product.get_all_products()
        categories = Category.get_all_categories()

        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are:', request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self,request):
        product = request.POST.get('product')
        cart = request.session.get("cart")
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity + 1
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print("cart:",request.session['cart'])

        # print('product',product)
        return redirect("homepage")
        


# def index(request):
#     products = Product.get_all_products()
#     categories = Category.get_all_categories()

#     data = {}
#     data['products'] = products
#     data['categories'] = categories
#     print('you are:', request.session.get('email'))
#     return render(request, 'index.html', data)


# def signup(request):
#     if(request.method == "GET"):
#         return render(request, 'signup.html')
#     else:
#          return registerUser(request)

class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get("firstname")
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        v1 = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)

        # saving
        if not error_message:
            # print(first_name,last_name,password)
            customer.password = make_password(customer.password)

            customer.register()

            return redirect('homepage')
        else:
            data = {
                "error": error_message,
                "values": v1
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None

        if(not customer.first_name):
            error_message = "First name required"
        elif len(customer.first_name) < 4:
            error_message = "First name should be atleast 4 in length"
        elif not customer.last_name:
            error_message = "Last Name required"
        elif len(customer.last_name) < 4:
            error_message = "Last name should be atleast 4 in length"
        elif not customer.phone:
            error_message = "Phone number is required"
        elif len(customer.phone) < 10:
            error_message = "Phone number must be 10 character long"
        elif len(customer.password) < 6:
            error_message = "Password must be 6 character long"
        elif len(customer.email) < 5:
            error_message = "Email must be 5 character long"
        elif customer.isExists():
            error_message = "This email is already registered"

        return error_message


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                return redirect("homepage")
            else:
                error_message = "email or password invalid"
        else:
            error_message = "email or password invalid"

        print(customer)
        return render(request, 'login.html', {"error": error_message})


# def login(request):
#     if request.method == "GET":
#         return render(request,'login.html')

#     else:
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         customer = Customer.get_customer_by_email(email)
#         error_message = None

#         if customer:
#             flag = check_password(password,customer.password)
#             if flag:
#                 return redirect("homepage")
#             else:
#                 error_message = "email or password invalid"
#         else:
#             error_message = "email or password invalid"

#         print(customer)
#         return render(request,'login.html',{"error":error_message})
