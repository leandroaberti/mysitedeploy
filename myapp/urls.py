from django.contrib import admin
from django.urls import path
from . import views

#namespace
app_name = 'myapp'

urlpatterns = [
    path('', views.teste, name=''),
    #path('products/', views.ProductLisView.as_view(), name='products'),
    path('products/', views.products, name='products'),
    #path('products/<int:id>/', views.product_detail, name='productdetail'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='productdetail'),
    #path('products/add/', views.add_product, name='add_product'),
    path('products/add/', views.ProductAdd.as_view(), name='add_product'),
    #path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('products/update/<int:pk>/', views.ProductUpdate.as_view(), name='update_product'),
    #path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/delete/<int:pk>/', views.ProductDelete.as_view(), name='delete_product'),
    path('products/mylistings', views.my_listings, name='mylistings'),
    path('products/mylistingsdelete/<int:id>/', views.my_listings_delete, name='mylistingsdelete'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
    # api view
    path('api/checkout-session/<id>',views.create_checkout_session, name='api_checkout_session'),
    path('api/checkout-show', views.checkout_show, name='checkout_show')
]