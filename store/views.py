from django.shortcuts import render, redirect,HttpResponseRedirect
from store.models import Product, Category, Customer, Order
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.views import View
from middleware.auth import auth_middleware
from django.utils.decorators import method_decorator

def get_data(data):
    if data:
        return Product.objects.filter(category=data)
    else:
        return Product.objects.all()


class addcart(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
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
        return redirect('addcart')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}

        products = None
        categorys = Category.objects.all()
        categorysid = request.GET.get('category')
        if categorysid:
            products = Product.objects.filter(category=categorysid)

        else:
            products = Product.objects.all()

        data = {}
        data['products'] = products
        data['categorys'] = categorys
        return render(request, 'product.html', data)


class cart_view(View):
    def get(self, request):
        login = request.session.get('customer')
        if login:
            ids = list(request.session.get('cart').keys())
            products = Product.objects.filter(id__in=ids)
            return render(request, 'cart.html', {'products': products})
        else:
            return redirect('login')


class checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=list(cart.keys()))
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))

            order.save()
        request.session['cart'] = {}
        return redirect('cart_view')


class order_view(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        customerid=request.session.get('customer')
        orders=Order.objects.filter(customer=customerid).order_by('-date')
        print(orders)
        return render(request,'order.html',{'orders':orders})


def signup_view(request):
    if request.method == 'POST':
        data = request.POST
        fname = data.get('firstname')
        lname = data.get('lastname')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        error_msg = None
        if len(fname) < 3:
            error_msg = "First name is not valid"
        elif len(lname) < 3:
            error_msg = "Last Name is not Valid"
        elif len(phone) < 9:
            error_msg = 'Phone Number is not Valid'
        elif len(password) < 7:
            error_msg = 'Password Is not Valid'
        elif Customer.objects.filter(email=email):
            error_msg = 'Email exits'

        value = {
            'first_name': fname,
            'last_name': lname,
            'phone': phone,
            'email': email
        }

        if not error_msg:
            customers = Customer(first_name=fname,
                                 last_name=lname,
                                 phone=phone,
                                 email=email,
                                 password=password)
            customers.password = make_password(customers.password)
            customers.save()
            return redirect('product')
        else:
            error = {
                'error': error_msg,
                'values': value
            }
            return render(request, 'signup.html', error)
    return render(request, 'signup.html')


def logout_view(request):
    request.session.clear()
    return render(request, 'logout.html')


def login_view(request):
    returnUrl=None
    if request.method == "GET":
        login_view.returnUrl=request.GET.get('returnUrl')
        print("Get")
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_message = None
        try:
            customers = Customer.objects.get(email=email)
        except:
            customers = False
        if customers:
            flag = check_password(password, customers.password)
            if flag:
                request.session['customer'] = customers.id
                request.session['email'] = customers.email

                if login_view.returnUrl:
                    return HttpResponseRedirect(login_view.returnUrl)
                else:
                    login_view.returnUrl=None
                    return redirect('addcart')
            else:
                error_message = "Password Not Matched"
        else:
            error_message = "Credential Not Matched "
        return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
