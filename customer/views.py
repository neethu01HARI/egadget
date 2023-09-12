from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
from django.views.generic import TemplateView,View,ListView,DetailView
from django.shortcuts import render
from account.models import Products,Cart,Order
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# decorator
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please login first")
            return redirect("ehm")
    return inner

decs=[never_cache,signin_required]
# class CustomerHomeView(TemplateView):
#     template_name="cust_home.html"

@method_decorator(decs,name='dispatch')
class CustomerHomeView(ListView):
    template_name="cust_home.html"
    queryset=Products.objects.all()
    context_object_name="products"

# class ProductDetailView(View):
#     def get(self,request,**kwargs):
#         pid=kwargs.get('id')
#         pro=Products.objects.get(id=pid)
#         return render(request,"product_details.html",{"data":pro})

@method_decorator(decs,name='dispatch')  
class ProductDetailView(DetailView):
    template_name="product_details.html"
    pk_url_kwarg='id'
    queryset=Products.objects.all()
    context_object_name='data'

decs
def addcart(request,*args,**kwargs):
    id=kwargs.get("id")
    pro=Products.objects.get(id=id)
    user=request.user
    qty=request.POST.get('qnt')
    Cart.objects.create(product=pro,user=user,quantity=qty)
    messages.success(request,"Item Added to Cart")
    return redirect('custhome')





@method_decorator(decs,name='dispatch')
class CartListView(ListView):
    template_name="cart.html"
    queryset=Cart.objects.all()
    context_object_name="cart"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,status='cart')
    
# for remove
decs
def removecart(request,**kwargs):
    pid=kwargs.get("id")
    c=Cart.objects.get(id=pid)
    c.delete()
    messages.success(request,"Cart Item Removed!")
    return redirect('clist')

@method_decorator(decs,name='dispatch')
class PaymetView(TemplateView):
    template_name="payment.html"

    def post(self,request,*args,**kwargs):
        cid=kwargs.get("id")
        cart=Cart.objects.get(id=cid)
        ad=request.POST.get("address")
        ph=request.POST.get("phone")
        Order.objects.create(cart=cart,address=ad,phone=ph)
        cart.status='Order Placed'
        cart.save()
        messages.success(request,"order placed successfully")
        return redirect("clist")
    

# class OrderListView(TemplateView):
#     template_name="order.html"
@method_decorator(decs,name='dispatch')
class OrderListView(ListView):
    template_name="order.html"
    queryset=Order.objects.all()
    context_object_name="order"

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)
    
decs
def cancelorder(request,*args,**kwargs):
    oid=kwargs.get("id")
    order=Order.objects.get(id=oid)
    order.status='Cancelled'
    order.save()
    messages.success(request,"Order Cancelled ")
    return redirect('olist')
