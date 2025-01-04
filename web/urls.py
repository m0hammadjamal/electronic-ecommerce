from django.urls import path
from web import views

app_name = 'web'

urlpatterns = [
    path('',views.index, name='index'),
    path('account/',views.account, name='account'),

    path('cart/',views.cart, name='cart'),
    path('add/to/cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('cart/plus/<int:id>/',views.cart_plus,name='cart_plus'),
    path('cart/minus/<int:id>/',views.cart_minus,name='cart_minus'),

    path("addresses/", views.manage_addresses, name="manage_addresses"),
    path("addresses/add/", views.add_address, name="add_address"),
    path("addresses/<int:id>/edit/", views.edit_address, name="edit_address"),
    path("addresses/<int:id>/delete/", views.delete_address, name="delete_address"),

    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('verify/register/<str:email>/', views.verify_register, name='verify_register'),  # OTP verification page
    path('logout/', views.user_logout, name='logout'),
    path('resend/otp/<str:email>/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('order/<int:id>/',views.order, name='order'),
    path('orders/',views.orders, name='orders'),

    path('category/<int:id>/',views.category, name='category'),
    path('brand/<int:id>/',views.brand, name='brand'),

    path('product/<int:id>/',views.product, name='product'),
    path('product/<int:id>/add/review/', views.add_review, name='add_review'),

    path('service/',views.services, name='service'),
    path('request/service/', views.request_service, name='request_service'),

    path('whishlist/',views.whishlist, name='whishlist'),
    path('add/to/wishlist/<int:id>/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]