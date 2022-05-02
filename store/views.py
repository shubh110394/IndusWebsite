from ast import Or
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from store.models.orders import Order
from store.models.prevorder import Previous
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View
import random as r

from store.models import customer
import razorpay
#for pdf generation
from django.http import FileResponse
from django.template.loader import get_template
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
from xhtml2pdf import pisa

# Create your views here

class Index(View):
    def get(self, request):
        cus_id = request.session.get("customer")
        customer = Customer.get_customers_by_id(cus_id)
        dict_val = {}
        for cus in customer:
            # print(cus)
            dict_val['address1'] = cus.address1
            dict_val['address2'] = cus.address2
            dict_val['address3'] = cus.address3
        # ids = list(request.session.get("cart"))
        # products = Product.get_all_products_by_id(ids)
        # para = {
        #     "dict_val" :dict_val,
        #     'products':products,
        #     'id':ids
        # }

        cart = request.session.get("cart")
        if not cart:
            request.session['cart'] = {}
        # products = Product.get_all_products()
        products = None
        categories = Category.get_all_categories()
        # categoryId = request.GET.get('category')
        # if categoryId:
        #     Product.get_all_products()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.get_all_products_category_by_id(category_id)
        else:
            products = Product.get_all_products()

        data = {
            "dict_val": dict_val,
            'products': products,
            # 'id':ids
        }
        data['products'] = products
        data['categories'] = categories
        # print('you are:', request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        product_id = request.POST.get("product_key")
        cart = request.session.get("cart")
        quantity = None

        customer = request.session.get("customer")
        if product_id:
            if customer:

                orders = Order.get_orders_by_customer(
                    customer)
                customerObj = Customer.get_customers_by_id(customer)
                dict_val = {}
                for cus in customerObj:
                    dict_val['address1'] = cus.address1
                    dict_val['address2'] = cus.address2
                    dict_val['address3'] = cus.address3

                order_id = r.randint(1000000000, 9000000000)
                products = Product.get_all_products_by_id(product_id)
                for product in products:
                    order = Order(customer=Customer(id=customer), product=product, price=product.price,
                                  quantity=1, order_id=order_id)
                    order.save()

                    history = Previous(customer=Customer(id=customer), product=product, price=product.price,
                                       quantity=1, order_id=order_id)
                    history.save()
                order_dict = {
                    'orders': orders,
                    # 'dict_val':dict_val
                }
                # return render(request,"orders.html",order_dict)
                return redirect("orders")
            else:
                return redirect("login")
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
        request.session['quantity'] = quantity
        return redirect("homepage")


class Search(View):

    def get(self, request):
        query = request.GET.get("query")
        cus_id = request.session.get("customer")
        customer = Customer.get_customers_by_id(cus_id)
        dict_val = {}
        for cus in customer:
            dict_val['address1'] = cus.address1
            dict_val['address2'] = cus.address2
            dict_val['address3'] = cus.address3

        cart = request.session.get("cart")
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.get_all_products_category_by_id(category_id)
        else:
            products = Product.get_all_products()

        if query:
            products = Product.objects.filter(name__icontains=query)
            if not products:
                products = 'false'

        # def searchMatch(query,item):

        #     if Product.objects.filter(name__icontains = query) or Product.objects.filter(category__icontains = query) or Product.objects.filter(price__icontains = query):
        #         return True
        #     if not products:
        #             products = 'false'
        #     else:
        #         return False

        # products = [item for item in products if searchMatch(query,item)]

        data = {
            "dict_val": dict_val,
            'products': products,
            # 'id':ids
        }
        data['products'] = products
        data['categories'] = categories
        return render(request, 'search.html', data)

    def post(self, request):
        product = request.POST.get('product2')
        remove = request.POST.get('remove')
        product_id = request.POST.get("product_key")
        cart = request.session.get("cart")
        quantity = None

        customer = request.session.get("customer")
        if product_id:
            if customer:

                orders = Order.get_orders_by_customer(
                    customer)
                customerObj = Customer.get_customers_by_id(customer)
                dict_val = {}
                for cus in customerObj:
                    dict_val['address1'] = cus.address1
                    dict_val['address2'] = cus.address2
                    dict_val['address3'] = cus.address3

                order_id = r.randint(1000000000, 9000000000)
                products = Product.get_all_products_by_id(product_id)
                for product in products:
                    order = Order(customer=Customer(id=customer), product=product, price=product.price,
                                  quantity=1, order_id=order_id)
                    order.save()

                    history = Previous(customer=Customer(id=customer), product=product, price=product.price,
                                       quantity=1, order_id=order_id)
                    history.save()
                order_dict = {
                    'orders': orders,
                }

                return redirect("orders")
            else:
                return redirect("login")
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
        request.session['quantity'] = quantity
        return redirect("search")


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
        welcome = None
        if not error_message:
            # print(first_name,last_name,password)
            customer.password = make_password(customer.password)
            welcome = "Successfull"
            customer.register()
            # return redirect('login')
            context = {
                'welcome' : welcome
            }
            print(context)
            return render(request, 'signup.html', context)
        else:
            data = {
                "error": error_message,
                "values": v1
            }
            return render(request, 'signup.html', data)
        # return redirect('login')

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
        # Login.return_url = request.GET.get('return_url')
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
                # if Login.return_url:
                #     return HttpResponseRedirect(Login.return_url)
                # else:
                #     Login.return_url = None
                return redirect("homepage")
            else:
                error_message = "password invalid"
        else:
            error_message = "email not registered"

        print(customer)
        return render(request, 'login.html', {"error": error_message})


def logout(request):
    request.session.clear()
    # return HttpResponse("hi")
    return redirect("homepage")


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
                dict_val['address1'] = cus.address1
                dict_val['address2'] = cus.address2
                dict_val['address3'] = cus.address3
            ids = list(request.session.get("cart"))
            products = Product.get_all_products_by_id(ids)
            para = {
                'products': products,
                'id': ids
            }
            return render(request, 'cart.html', para)

    def post(self, request):
        customer = request.session.get('customer')
        products = None
        # price = None
        phone = 1234
        cart = request.session.get('cart')
        order_id = r.randint(1000000000, 9000000000)
        address = None
        radio_val = None
        products = Product.get_all_products_by_id(list(cart.keys()))
        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price,
                          phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
            order.save()

            history = Previous(customer=Customer(id=customer), product=product, price=product.price,
                               phone=phone, quantity=cart.get(str(product.id)), order_id=order_id)
            history.save()
        # return render(request,'orders.html')
        request.session['cart'] = {}
        return redirect("orders")

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
            Customer.objects.filter(id=customer).update(address1=address_post1)
            phone = request.POST.get('phone')
            request.session['address'] = address
            # products = Product.get_all_products_by_id(list(cart.keys()))
            # order_id = r.randint(1000000000, 9000000000)

            # request.session['cart'] = {}
            # return redirect("orders")
        if request.POST.get("address_post2"):
            address_post2 = request.POST.get("address_post2")
            address = address_post2
            Customer.objects.filter(id=customer).update(address2=address_post2)
            phone = request.POST.get('phone')
            request.session['address'] = address

        if request.POST.get("address_post3"):
            address_post3 = request.POST.get("address_post3")
            address = address_post3
            Customer.objects.filter(id=customer).update(address3=address_post3)
            phone = request.POST.get('phone')
            request.session['address'] = address


class Orders(View):

    # @method_decorator(auth_middleware)
    # order_id = None
    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        customerObj = Customer.get_customers_by_id(customer)
        orders = Order.get_orders_by_customer(
            customer)  # taking from model Order
        order_id = r.randint(1000000000, 9000000000)

        dict_val = {}
        for cus in customerObj:
            dict_val['address1'] = cus.address1
            dict_val['address2'] = cus.address2
            dict_val['address3'] = cus.address3
        # print(orders)
        order_dict = {
            'orders': orders,
            'order_id': order_id,
            'dict_val': dict_val
        }
        return render(request, 'orders.html', order_dict)

    def post(self, request):
        customer = request.session.get("customer")

        if request.POST.get("flexRadioDefault"):
            print("hi")
            radio_val = request.POST.get("flexRadioDefault")
            address = radio_val
            request.session['address'] = address
            return redirect('payment')

        if request.POST.get("address_post1"):
            address_post1 = request.POST.get("address_post1")
            address = address_post1
            Customer.objects.filter(id=customer).update(address1=address_post1)
            phone = request.POST.get('phone')
            request.session['address'] = address
            return redirect('payment')

        if request.POST.get("address_post2"):
            address_post2 = request.POST.get("address_post2")
            address = address_post2
            Customer.objects.filter(id=customer).update(address2=address_post2)
            phone = request.POST.get('phone')
            request.session['address'] = address
            return redirect('payment')

        if request.POST.get("address_post3"):
            address_post3 = request.POST.get("address_post3")
            address = address_post3
            Customer.objects.filter(id=customer).update(address3=address_post3)
            phone = request.POST.get('phone')
            request.session['address'] = address
            return redirect('payment')


# Adding payment gateway

class Payment(View):
    order_dict = {
    }

    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        add = request.session.get('address')
        orders = Order.get_orders_by_customer(
            customer)  # taking from model Order
        total = 0
        for order in orders:
            num = order.quantity
            price = num * order.price
            total += price
        ultimate_total = 0
        gst = Payment.gst_price(total)

        request.session['tax_gst'] = gst
        nam = ""
        for order in orders:
            nam += order.product.name + ","
            Payment.order_dict['product'] = nam
            Payment.order_dict['total'] = total
            Payment.order_dict['date'] = order.date
            Payment.order_dict['orderId'] = order.order_id
            Payment.order_dict['tax'] = Payment.gst_price(total)
            Payment.order_dict['toPay'] = Payment.gst_price(
                total) + total + 100
            ultimate_total = Payment.gst_price(total) + total + 100
            Payment.order_dict['address'] = add
        # print(Payment.order_dict)
        request.session['ultimate_total'] = ultimate_total
        return render(request, 'payment.html', Payment.order_dict)

    def post(self, request):
        value = request.POST.get("flexRadioDefault")
        payment_method = request.POST.get("payment_method")
        # payment_method = value
        customer = request.session.get("customer")
        customer_details = Customer.get_customers_by_id(customer)
        home = request.POST.get("gohome")

        cus_name = None
        cus_email = None
        cus_phone = None
        for cus in customer_details:
            cus_name = cus.first_name
            cus_email = cus.email
            cus_phone = cus.phone
        orders = Order.get_orders_by_customer(
            customer)
        
        error_message = None
        total = 0
        for order in orders:
            num = order.quantity
            price = num * order.price
            total += price
        if home:
            records = Order.objects.all()
            Previous.status = True
            Payment.order_dict['value'] = None
            records.delete()
            return redirect('homepage')

        if value == None and payment_method == None:
                error_message = "choose atleast one method"
                Payment.order_dict['error_message'] = error_message
                Payment.order_dict['value'] = value
                return render(request, 'payment.html', Payment.order_dict)
        if value != None:
                error_message = None
                Payment.order_dict['error_message'] = error_message
                Payment.order_dict['value'] = value
                return render(request, 'payment.html', Payment.order_dict)
 

        # if value:
            

        #     if value == None:
        #         error_message = "choose atleast one method"
        #         Payment.order_dict['error_message'] = error_message
        #         return render(request, 'payment.html', Payment.order_dict)
            
        #     if value != None:
        #         Payment.order_dict['value'] = value
        #         return render(request, 'payment.html', Payment.order_dict)
        

            

        if payment_method:

            if payment_method == "Cash":
                    records = Order.objects.all()
                    Previous.status = True
                    records.delete()
                    return redirect("homepage")
            if payment_method == "Razorpay":
                client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
                data = {"amount": total * 100, "currency": "INR",'payment_capture':1}
                payment = client.order.create(data=data)
                orders.razorpay_order_id = payment['id']
                Payment.order_dict['value'] = None
                Order.place_order
                print('payment', payment)
                # Payment.order_dict['payment'] = payment
                # return redirect('success')
                return render(request,'payment_sum_razor.html',{'payment':payment,'total':total})
        else:
            print(value)
            records = Order.objects.all()
            Previous.status = True
            records.delete()
            return redirect('homepage')

        # else:
        #     if payment_method == "Cash" or payment_method == None:
        #         records = Order.objects.all()
        #         Previous.status = True
        #         records.delete()
        #         return redirect("homepage")
        #     else:
        #         return redirect('razorInte')

                # client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
                # data = {"amount": total * 100, "currency": "INR",'payment_capture':1}
                # payment = client.order.create(data=data)
                # orders.razorpay_order_id = payment['id']
                # Order.place_order
                # print('payment', payment)
                # # Payment.order_dict['payment'] = payment
                # return render(request,'payment_sum_razor.html',{'payment':payment,'total':total})

    @staticmethod
    def gst_price(price):
        after_tax = 0.12 * price
        return after_tax

def razorInte(request):
    # if request.method == "POST":
    #             # key_id = 'rzp_test_nFQnwxZOOLoAND'
    #             # key_secret = 'xHH4R8bNVv7bOjsoKnpC0n0H'

    #             client = razorpay.Client(auth=(key_id, key_secret))

    #             data = {"amount": 500 * 100, "currency": "INR",'payment_capture':1}
    #             payment = client.order.create(data=data)
    #             # order_obj.razorpay_order_id = payment['id']
    #             # order_obj.save()
    #             print('payment', payment)

    # return render(request,'payment_sum_razor.html')
    pass
                

class History(View):
    def get(self, request):
        # for finding out which customer is trying to checkout
        customer = request.session.get("customer")
        history = Previous.get_orders_by_customer(
            customer)  # taking from model Order
        # order_id = r.randint(1000000000, 9000000000)
        print(history)

        order_dict = {
            'orders': history
        }
        return render(request, 'orderHistory.html', order_dict)

def success(request):
    if request.method == "POST":
            order_id = request.GET.get('order_id')
            records = Order.objects.all()
            records.delete()
            Previous.status_change(order_id)
            return redirect("homepage")
    else:
        order_id = request.GET.get('order_id')
        customer = request.session.get("customer")
        orders = Order.get_orders_by_customer(
            customer) 
        context = {}
        total = 0
        trans_id = None
        for order in orders:
            num = order.quantity
            price = num * order.price
            total += price
            trans_id = order.razorpay_order_id
        
        request.session['transaction_id'] = trans_id
        price = request.session.get('ultimate_total')
        context = {
            'ultimate_total' : price,
            'total':total,
            'tax': 0.12 * total,
        }
        nam = ""
        for order in orders:
            nam += order.product.name + ","
            context['product'] = nam
            context['date'] = order.date
            context['orderId'] = order.order_id
        # print(context)
        Previous.status_change(order_id)
        return render(request,'success.html',context)



def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class ViewPdf(View):
    def get(self,request,*args,**kwargs):
            customer = request.session.get("customer")
            pdf_data = Order.get_orders_by_customer(customer)
            lines = {}
            add = request.session.get('address')
            for p in pdf_data:
                lines['Customer_name'] = p.customer.first_name
                lines['surname'] = p.customer.last_name
                lines['product_name'] = p.product.name
                lines['order_date'] = p.date
                lines['order_id'] = p.order_id
                lines['gross_total'] = p.price
                lines['shipping_charges'] = 100
                lines['tax'] = p.price * 0.12
                lines['to_pay'] = request.session.get('ultimate_total')
                lines['address'] = add
            print(pdf_data,lines)
            lines['pdf_data'] = pdf_data
            pdf = render_to_pdf('pdf_template.html',lines)
            return HttpResponse(pdf,content_type = 'application/pdf')

# def Search(request):

#             query = request.GET.get("query")
#             remove = request.POST.get('remove')

#             category_id = request.GET.get('category')
#             cus_id = request.session.get("customer")
#             customer = Customer.get_customers_by_id(cus_id)
#             dict_val = {}
#             for cus in customer:
#                 dict_val['address1'] = cus.address1
#                 dict_val['address2'] = cus.address2
#                 dict_val['address3'] = cus.address3

#             cart = request.session.get("cart")
#             if not cart:
#                 request.session['cart'] = {}
#             if cart:
#                 quantity = cart.get(product)
#                 if quantity:
#                     if remove:
#                         if quantity <= 1:
#                             cart.pop(product)
#                         else:
#                             cart[product] = quantity - 1
#                     else:
#                         cart[product] = quantity + 1
#                 else:
#                     cart[product] = 1

#             else:
#                 cart = {}
#                 cart[product] = 1
#             products = None
#             if query:
#                 products = Product.objects.filter(name__icontains = query)
#                 if not products:
#                     products = 'false'
#             categories = Category.get_all_categories()

#             data = {
#                 "dict_val": dict_val,
#                 'products': products,
#                 'query':query
#             }

#             data['categories'] = categories
#             print('type',type(data['categories']))
#             return render(request, 'search.html', data)
