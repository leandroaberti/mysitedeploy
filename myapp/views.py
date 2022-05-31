#from itertools import product
from math import prod
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.http import HttpResponse
from .models import OrderDetail, Product

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView #CRUD

from django.urls import reverse, reverse_lazy

#integrated STRIPE PAYMENT GATEWAY
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

import stripe

# Create your views here.
def teste(request):
    return HttpResponse("Hello!")


def products(request):
    
    page_obj = products = Product.objects.all()
    
    #search name
    product_name = request.GET.get('product_name')
    
    if product_name != '' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
        
    
    paginator = Paginator(page_obj, 3)
    #paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        #'products': products,
        'page_obj': page_obj,
    }
    return render(request, 'myapp/index.html', context)

    #return HttpResponse(productList)

def product_detail(request,id):
    product = Product.objects.get(id=id)

    context = {
        'product': product
    }
    
    return render(request, 'myapp/detail.html', context)

    #return HttpResponse('The product id is: ' + str(id))

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(name=name, price=price, description=description, image=image, seller_name=seller_name)
        product.save()

        if product.id: 
            return my_listings(request)


    return render(request, 'myapp/addproduct.html')


def update_product(request, id):
    product = Product.objects.get(id=id)
    
    if request.method == 'POST':
        
        if request.POST.get('name') is not None: product.name = request.POST.get('name')
        if request.POST.get('price') is not None: product.price = request.POST.get('price')
        if request.POST.get('price') is not None: product.description = request.POST.get('description')
        if request.FILES.get('upload') is not None: product.image = request.FILES.get('upload') 
        product.save()

        # redirect to another page
        return redirect('/myapp/products')

    context = {
        'product': product,
    }
    return render(request, 'myapp/updateproduct.html', context)

def delete_product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product':product,
    }

    if request.method == 'POST':
        product.delete()
        return redirect('/myapp/products')


    return render(request, 'myapp/delete.html', context)


def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products':products
    }
    
    return render(request, 'myapp/mylistings.html', context)

def my_listings_delete(request, id):
    
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
    
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products':products
    }
    
    return render(request, 'myapp/mylistings.html', context)


#Class based view
class ProductLisView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 3
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'product'
    
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super (ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PK  # add Stripe Publishible Key
        return context
    
    
class ProductAdd(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'image', 'seller_name']
    #product_form.html
    
class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'image', 'seller_name']
    template_name_suffix = '_update_form'
    
    
class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:products')
    
    
@csrf_exempt
def create_checkout_session(request, id):
    
    product = get_object_or_404(Product, pk=id) #get the product or a 404 page
   
    # setup stripe payment session
    stripe.api_key = settings.STRIPE_SK
    checkout_session  = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency':'usd',
                    'product_data': {
                        'name':product.name,
                    },
                    'unit_amount':int(product.price * 100)
                },
                'quantity': 1,
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('myapp:failed')),
    )
    
   # print('session: ',checkout_session)

    # fill in order detail
    order = OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    
    print('session: ',{'sessionId':checkout_session.id})
    
    
    return JsonResponse({'sessionId':checkout_session.id})



def checkout_show(request):
    
    if request.method == 'POST':
        checkout_url = request.POST.get('url')
        return redirect(checkout_url)
    return redirect('myapp:products')



class PaymentSuccessView(TemplateView):
    template_name = 'myapp/payment_success.html'
    
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SK
        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)
   
class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'     