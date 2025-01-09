from django.db import models
from main.models import CommonModel
from users.models import User
from items.models import *

ADDRESS_TYPE_CHOICE = (
    ("HM", "Home"),
    ("WO", "Work"),
    ("OT", "Other")
)

ORDER_STATUS = (
    ('IN', 'Initiated'),
    ('PL', 'Placed'),
    ('IP', 'In progress'),
    ('DI', 'Dispatched'),
    ('CO', 'Completed'),
    ('CA', 'Cancelled')
)



class Customer(CommonModel):
    customer_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customers_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ["-id"]

    def __str__(self):

        return f'{self.user.phone_number}-{self.user.email}'



class CartItem(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True)  # Optional for variants
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()  # Save the price at the time of adding to cart

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def total_price(self):
        return self.price * self.quantity
    


class Whishlist(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_whishlist'
        verbose_name = 'whishlist'
        verbose_name_plural = 'whishlists'
        ordering = ["-id"]

    def __str__(self):

        return self.customer.user.email
    



class Service(CommonModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    
    def __str__(self):
        return self.title

class ServiceRequest(CommonModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_service_request'
        verbose_name = 'service_request'
        verbose_name_plural = 'service_requests'
        ordering = ["-id"]

    def __str__(self):
        return self.service.title
    


class Coupon(CommonModel):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    is_Percentage = models.BooleanField(default=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_onece_peruser = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils.timezone import now
        return self.active and self.valid_from <= now() <= self.valid_until

    def __str__(self):
        return self.code
    


class Address(CommonModel):
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    pincode = models.CharField(max_length=25)
    address_type = models.CharField(max_length=255, choices=ADDRESS_TYPE_CHOICE,blank=True, null=True)
    is_default = models.BooleanField(default=False)
    class Meta:
        db_table = 'customers_address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        ordering = ["-id"]

    def __str__(self):

        return self.address1


class CartTotal(models.Model):
    item_total = models.FloatField(default=0)
    total = models.FloatField(default=0)
    offer = models.FloatField(default=0)
    delivery = models.FloatField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


    class Meta:
        db_table = 'Customer_CartTotal'
        verbose_name = 'carttotal'
        verbose_name_plural = 'carttotals'
        ordering = ['-id']


    def __str__(self):
        return self.customer.user.email
    


class OrderItem(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0)
    class Meta:
        db_table = 'customers_order_item'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        ordering = ["-id"]

    def __str__(self):

        return self.product.name
    

class Order(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=35)
    items = models.ManyToManyField(OrderItem)
    sub_total = models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0)
    offer = models.FloatField(default=0)
    total = models.FloatField(default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    order_status = models.CharField(max_length=25, choices=ORDER_STATUS ,default='IN')
    address1 = models.CharField(max_length=100,blank=True, null=True)
    address2 = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=25,blank=True, null=True)
    state = models.CharField(max_length=25,blank=True, null=True)
    pincode = models.CharField(max_length=25,blank=True, null=True)
    address_type = models.CharField(max_length=255, choices=ADDRESS_TYPE_CHOICE,blank=True, null=True)

    class Meta:
        db_table = 'customers_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ["-id"]

    def __str__(self):

        return self.order_id
    



class Review(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'customers_review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ["-id"]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"