from distutils.log import error
import email
from itertools import product
from wsgiref import validate
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from store.models import orders

from store.models.orders import Order
from store.models.prevorder import Previous
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View
import random as r
# from django.utils.decorators import method_decorator
# from store.middlewares.auth import auth_middleware


# Create your views here.

class Index(View):
    def get(self, request):
        cart = request.session.get("cart")
        if not cart:
            request.session['cart'] = {}
        products = Product.get_all_products()
        # products = None
        categories = Category.get_all_categories()
        # categoryId = request.GET.get('category')
        # if categoryId:
        #     Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories
        # print('you are:', request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get("cart")
        buy = request.POST.get('buy')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # print("cart:",request.session['cart'])

        if buy:
            if request.session.get("customer") == None:
                return redirect("login")
            else:
                pass
        # print('product',product)
        return redirect("homepage")

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
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer_name'] = customer.first_name
                # request.session['email'] = customer.email ##we commented this coz customer id is enough due to its uniqueness
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect("homepage")
            else:
                error_message = "email or password invalid"
        else:
            error_message = "email or password invalid"

        print(customer)
        return render(request, 'login.html', {"error": error_message})


def logout(request):
    request.session.clear()
    return redirect("login")



class Cart(View):
    def get(self, request):
        # print(list(request.session.get("customer")))
        # print(request.session.get("customer"))
        if request.session.get("customer") == None:
            return redirect("login")
        else:
            cus_id = request.session.get("customer")
            customer = Customer.get_customers_by_id(cus_id)
            dict_val = {}
            for cus in customer:
                # print(cus)
                dict_val['address1'] = cus.address1
                dict_val['address2'] = cus.address2
                dict_val['address3']  = cus.address3
            ids = list(request.session.get("cart"))
            products = Product.get_all_products_by_id(ids)
            para = {
                "dict_val" :dict_val,
                'products':products,
                'id':ids
            }
            return render(request, 'cart.html', para)
    def post(self,request):
        customer = request.session.get('customer')
        products = None
        # price = None
        phone = 1234
        cart = request.session.get('cart')
        order_id = r.randint(1000000000, 9000000000)
        address = None
        radio_val = None
        products = Product.get_all_products_by_id(list(cart.keys()))
        
        if request.POST.get("flexRadioDefault"):
            radio_val = request.POST.get("flexRadioDefault")
            address = radio_val
            request.session['address'] = address

            # address = value
            # phone = 12345
            # customer = request.session.get('customer')
            # cart = request.session.get('cart')
            # products = Product.get_all_products_by_id(list(cart.keys()))
            # print("address", phone, customer, cart, products)
            # order_id = r.randint(1000000000, 9000000000)

            # for product in products:
            #     order = Order(customer=Customer(id=customer), product=product, price=product.price,
            #                 phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
            #     order.save()

            # request.session['cart'] = {}     
            # return render(request,"orders.html",{'value':value})

        if request.POST.get("address_post1"):
            address_post1 = request.POST.get("address_post1")
            address = address_post1
            Customer.objects.filter(id = customer).update(address1 = address_post1)
            phone = request.POST.get('phone')
            request.session['address'] = address
            # products = Product.get_all_products_by_id(list(cart.keys()))
            # order_id = r.randint(1000000000, 9000000000)


            # request.session['cart'] = {}     
            # return redirect("orders")
        if request.POST.get("address_post2"):
            address_post2 = request.POST.get("address_post2")
            address = address_post2
            Customer.objects.filter(id = customer).update(address2 = address_post2)
            phone = request.POST.get('phone')
            request.session['address'] = address

        if request.POST.get("address_post3"):
            address_post3 = request.POST.get("address_post3")
            address = address_post3
            Customer.objects.filter(id = customer).update(address3 = address_post3)
            phone = request.POST.get('phone')
            request.session['address'] = address


        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price,
                            phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
            order.save()

            history = Previous(customer=Customer(id=customer), product=product, price=product.price,
                             phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
            history.save()

        request.session['cart'] = {}     
        return redirect("orders")
        


        

            



        


        



class CheckOut(View):
    def get(self,request):
        return HttpResponse("hey there")
    # def post(self, request):
    #     # request.Post gives the value whose key is address
    #     address = request.POST.get('address')
    #     phone = request.POST.get('phone')
    #     customer = request.session.get('customer')
    #     cart = request.session.get('cart')
    #     products = Product.get_all_products_by_id(list(cart.keys()))
    #     print(address, phone, customer, cart, products)
    #     order_id = r.randint(1000000000, 9000000000)

    #     for product in products:
    #         order = Order(customer=Customer(id=customer), product=product, price=product.price,
    #                       address=address, phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
    #         order.save()

    #     request.session['cart'] = {}

    #     return redirect("payment")
    


class Orders(View):

    # @method_decorator(auth_middleware)
    # order_id = None
    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        orders = Order.get_orders_by_customer(
            customer)  # taking from model Order
        # order_id = r.randint(1000000000, 9000000000)

        order_dict = {
            'orders': orders,
            # 'order_id': order_id
        }
        print(orders)
        return render(request, 'orders.html', order_dict)

    def post(self, request):
        order_id = request.POST.get("order_id")
        request.session['order'] = order_id
        # records = Order.objects.all()
        # records.delete()   
        return redirect('payment')



class Payment(View):

    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        add = request.session.get('address')
        orders = Order.get_orders_by_customer(
            customer)  # taking from model Order
        total = 0
        order_dict = {
        }
        for order in orders:
            num = order.quantity
            price = num * order.price
            total += price
        for order in orders:
            order_dict['product'] = order.product
            order_dict['total'] = total
            order_dict['date'] = order.date
            order_dict['orderId'] = order.order_id
            order_dict['tax'] = Payment.gst_price(total)
            order_dict['toPay'] = Payment.gst_price(total) + total + 100
            order_dict['address'] = add
        # print(order_dict)
        return render(request, 'payment.html', order_dict)

    def post(self, request):
        value = request.POST.get("flexRadioDefault")
        if request.POST.get("flexRadioDefault"):
            value = request.POST.get("flexRadioDefault")
            print(value)

        else:
            records = Order.objects.all()
            records.delete()   
        # return render(request, 'payment.html', {'value': value})
        return redirect("homepage")

    @staticmethod
    def gst_price(price):
        after_tax = 0.12 * price
        return after_tax


class History(View):
    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        history = Previous.get_orders_by_customer(customer)  # taking from model Order
        # order_id = r.randint(1000000000, 9000000000)
        print(history)
    
        

        order_dict = {
            'orders':history
        }
        return render(request, 'orderHistory.html', order_dict)