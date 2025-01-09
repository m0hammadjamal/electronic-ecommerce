from django.urls import  path

from managers import views

app_name = 'managers'


urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    path('order/<int:id>/', views.order, name="order"),
    path('reports/', views.reports, name="reports"),
    path('settings/', views.settings, name="settings"),
    path('password/', views.password, name="password"),    
    path('customer/orders/<int:id>/', views.customer_order, name="customer_order"),

    path("order/accept/<int:id>/", views.order_accept, name="order_accept"),
    path("order/reject/<int:id>/", views.order_reject, name="order_reject"),
    path("order/dispatched/<int:id>/", views.order_dispatched, name="order_dispatched"),
    path("order/completed/<int:id>/", views.order_completed, name="order_completed"),

    # Category
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.categories_add, name='categories_add'),
    path('categories/edit/<int:id>/', views.categories_edit, name='categories_edit'),
    path('categories/delete/<int:id>/', views.categories_delete, name='categories_delete'),

    # Brand
    path('brands/', views.brands, name='brands'),
    path('brands/add/', views.brands_add, name='brands_add'),
    path('brands/edit/<int:id>/', views.brands_edit, name='brands_edit'),
    path('brands/delete/<int:id>/', views.brands_delete, name='brands_delete'),

    # Color
    path('colors/', views.colors, name='colors'),
    path('colors/add/', views.colors_add, name='colors_add'),
    path('colors/edit/<int:id>/', views.colors_edit, name='colors_edit'),
    path('colors/delete/<int:id>/', views.colors_delete, name='colors_delete'),

    # Custom Specification
    path('custom-specifications/', views.custom_specifications, name='custom_specifications'),
    path('custom-specifications/add/', views.custom_specifications_add, name='custom_specifications_add'),
    path('custom-specifications/edit/<int:id>/', views.custom_specifications_edit, name='custom_specifications_edit'),
    path('custom-specifications/delete/<int:id>/', views.custom_specifications_delete, name='custom_specifications_delete'),

    # Product
    path('products/', views.products, name='products'),
    path('products/add/', views.products_add, name='products_add'),
    path('products/edit/<int:id>/', views.products_edit, name='products_edit'),
    path('products/delete/<int:id>/', views.products_delete, name='products_delete'),

    # Option
    path('options/', views.options, name='options'),
    path('options/add/', views.options_add, name='options_add'),
    path('options/edit/<int:id>/', views.options_edit, name='options_edit'),
    path('options/delete/<int:id>/', views.options_delete, name='options_delete'),

    # Product Image
    path('product-images/', views.product_images, name='product_images'),
    path('product-images/add/', views.product_images_add, name='product_images_add'),
    path('product-images/edit/<int:id>/', views.product_images_edit, name='product_images_edit'),
    path('product-images/delete/<int:id>/', views.product_images_delete, name='product_images_delete'),

    # Ram
    path('rams/', views.rams, name='rams'),
    path('rams/add/', views.rams_add, name='rams_add'),
    path('rams/edit/<int:id>/', views.rams_edit, name='rams_edit'),
    path('rams/delete/<int:id>/', views.rams_delete, name='rams_delete'),

    # Storage
    path('storages/', views.storages, name='storages'),
    path('storages/add/', views.storages_add, name='storages_add'),
    path('storages/edit/<int:id>/', views.storages_edit, name='storages_edit'),
    path('storages/delete/<int:id>/', views.storages_delete, name='storages_delete'),

    # Icon Image
    path('icon-images/', views.icon_images, name='icon_images'),
    path('icon-images/add/', views.icon_images_add, name='icon_images_add'),
    path('icon-images/edit/<int:id>/', views.icon_images_edit, name='icon_images_edit'),
    path('icon-images/delete/<int:id>/', views.icon_images_delete, name='icon_images_delete'),

    # Spec
    path('specs/', views.specs, name='specs'),
    path('specs/add/', views.specs_add, name='specs_add'),
    path('specs/edit/<int:id>/', views.specs_edit, name='specs_edit'),
    path('specs/delete/<int:id>/', views.specs_delete, name='specs_delete'),

    # Customer
    path('customers/', views.customers, name='customers'),
    path('customers/add/', views.customers_add, name='customers_add'),
    path('customers/edit/<int:id>/', views.customers_edit, name='customers_edit'),
    path('customers/delete/<int:id>/', views.customers_delete, name='customers_delete'),

    # Cart Item
    path('cart-items/', views.cart_items, name='cart_items'),
    path('cart-items/add/', views.cart_items_add, name='cart_items_add'),
    path('cart-items/edit/<int:id>/', views.cart_items_edit, name='cart_items_edit'),
    path('cart-items/delete/<int:id>/', views.cart_items_delete, name='cart_items_delete'),

    # Whishlist
    path('whishlist/', views.whishlist, name='whishlist'),
    path('whishlist/add/', views.whishlist_add, name='whishlist_add'),
    path('whishlist/edit/<int:id>/', views.whishlist_edit, name='whishlist_edit'),
    path('whishlist/delete/<int:id>/', views.whishlist_delete, name='whishlist_delete'),

    # Service
    path('services/', views.services, name='services'),
    path('services/add/', views.services_add, name='services_add'),
    path('services/edit/<int:id>/', views.services_edit, name='services_edit'),
    path('services/delete/<int:id>/', views.services_delete, name='services_delete'),

    # Service Request
    path('service-requests/', views.service_requests, name='service_requests'),
    path('service-requests/add/', views.service_requests_add, name='service_requests_add'),
    path('service-requests/edit/<int:id>/', views.service_requests_edit, name='service_requests_edit'),
    path('service-requests/delete/<int:id>/', views.service_requests_delete, name='service_requests_delete'),
    path('request/<int:id>', views.request_service_detail_view, name='service_requests_details'),

    # Coupon
    path('coupons/', views.coupons, name='coupons'),
    path('coupons/add/', views.coupons_add, name='coupons_add'),
    path('coupons/edit/<int:id>/', views.coupons_edit, name='coupons_edit'),
    path('coupons/delete/<int:id>/', views.coupons_delete, name='coupons_delete'),

    # Address
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/add/', views.addresses_add, name='addresses_add'),
    path('addresses/edit/<int:id>/', views.addresses_edit, name='addresses_edit'),
    path('addresses/delete/<int:id>/', views.addresses_delete, name='addresses_delete'),

    # Cart Total
    path('cart-totals/', views.cart_totals, name='cart_totals'),
    path('cart-totals/add/', views.cart_totals_add, name='cart_totals_add'),
    path('cart-totals/edit/<int:id>/', views.cart_totals_edit, name='cart_totals_edit'),
    path('cart-totals/delete/<int:id>/', views.cart_totals_delete, name='cart_totals_delete'),

    # Order Item
    path('order-items/', views.order_items, name='order_items'),
    path('order-items/add/', views.order_items_add, name='order_items_add'),
    path('order-items/edit/<int:id>/', views.order_items_edit, name='order_items_edit'),
    path('order-items/delete/<int:id>/', views.order_items_delete, name='order_items_delete'),

    # Order
    path('orders/', views.orders, name='orders'),
    path('orders/add/', views.orders_add, name='orders_add'),
    path('orders/edit/<int:id>/', views.orders_edit, name='orders_edit'),
    path('orders/delete/<int:id>/', views.orders_delete, name='orders_delete'),

    # Review
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/add/', views.reviews_add, name='reviews_add'),
    path('reviews/edit/<int:id>/', views.reviews_edit, name='reviews_edit'),
    path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),

    # User
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='users_add'),
    path('users/edit/<int:pk>/', views.user_edit, name='users_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='users_delete'),

    # OTP Verifier
    path('otp-verifiers/', views.otpverifier_list, name='otpverifier_list'),

    # Slider
    path('sliders/', views.sliders, name='sliders'),
    path('sliders/add/', views.slider_add, name='sliders_add'),
    path('sliders/edit/<int:pk>/', views.slider_edit, name='sliders_edit'),
    path('sliders/delete/<int:pk>/', views.slider_delete, name='sliders_delete'),

    # Offer
    path('offers/', views.offer_list, name='offer'),
    path('offers/add/', views.offer_add, name='offer_add'),
    path('offers/edit/<int:pk>/', views.offer_edit, name='offer_edit'),
    path('offers/delete/<int:pk>/', views.offer_delete, name='offer_delete'),

    # Offers List
    path('offers-list/', views.offers_list, name='offers'),
    path('offers-list/add/', views.offers_add, name='offers_add'),
    path('offers-list/edit/<int:pk>/', views.offers_edit, name='offers_edit'),
    path('offers-list/delete/<int:pk>/', views.offers_delete, name='offers_delete'),
]