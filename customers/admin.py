from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(CartItem)
admin.site.register(Whishlist)
admin.site.register(Service)
admin.site.register(ServiceRequest)
admin.site.register(Coupon)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)