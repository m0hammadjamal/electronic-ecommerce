from django import forms
from django.contrib.auth.forms import UserCreationForm
from promos.models import *
from items.models import *
from users.models import *
from customers.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Brand Name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["color", "name"]
        widgets = {
            "color": forms.TextInput(attrs={"class": "form-control", "placeholder": "Color"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
        }

class CustomSpecificationForm(forms.ModelForm):
    class Meta:
        model = CustomSpecification
        fields = ["name", "key", "value"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Specification Name"}),
            "key": forms.TextInput(attrs={"class": "form-control", "placeholder": "Key"}),
            "value": forms.Textarea(attrs={"class": "form-control", "placeholder": "Value"}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "sku", "name", "description", "details", "mainimage", "regular_price", "sale_price",
            "offer_percentage", "video", "specifications", "category", "brand", "rating", "stock",
            "delivery_title", "delivery_duration", "garantee_title", "garantee_time", "sales_count"
        ]
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "SKU"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "details": forms.Textarea(attrs={"class": "form-control", "placeholder": "Details"}),
            "mainimage": forms.FileInput(attrs={"class": "form-control"}),
            "regular_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Regular Price"}),
            "sale_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Sale Price"}),
            "offer_percentage": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Offer Percentage"}),
            "video": forms.FileInput(attrs={"class": "form-control"}),
            "specifications": forms.SelectMultiple(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "brand": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Rating"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Stock"}),
            "delivery_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Delivery Title","value": "Free Delivery"}),
            "delivery_duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Delivery Duration","value": "1-2 day"}),
            "garantee_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guarantee Title","value": "Guaranteed"}),
            "garantee_time": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guarantee Time","value": "1 year"}),
            "sales_count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Sales Count"}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["name", "product", "color", "ram", "storage", "regular_price", "sale_price", "stock"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Option Name"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "color": forms.Select(attrs={"class": "form-control"}),
            "ram": forms.TextInput(attrs={"class": "form-control", "placeholder": "RAM"}),
            "storage": forms.TextInput(attrs={"class": "form-control", "placeholder": "Storage"}),
            "regular_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Regular Price"}),
            "sale_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Sale Price"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Stock"}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["product", "variant", "image", "alt_text"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "variant": forms.SelectMultiple(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "alt_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Alt Text"}),
        }

class RamForm(forms.ModelForm):
    class Meta:
        model = Ram
        fields = ["value"]
        widgets = {
            "value": forms.TextInput(attrs={"class": "form-control", "placeholder": "RAM Value"}),
        }

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ["value"]
        widgets = {
            "value": forms.TextInput(attrs={"class": "form-control", "placeholder": "Storage Value"}),
        }

class IconImageForm(forms.ModelForm):
    class Meta:
        model = IconImage
        fields = ["image", "name"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
        }

class SpecForm(forms.ModelForm):
    class Meta:
        model = Spec
        fields = ["product", "image", "detail"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "image": forms.Select(attrs={"class": "form-control"}),
            "detail": forms.TextInput(attrs={"class": "form-control", "placeholder": "Detail"}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_id", "user"]
        widgets = {
            "customer_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "Customer ID"}),
            "user": forms.Select(attrs={"class": "form-control"}),
        }

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["customer", "product", "option", "quantity", "price"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "option": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

class WhishlistForm(forms.ModelForm):
    class Meta:
        model = Whishlist
        fields = ["customer", "product"]  # Exclude 'added_on'
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "description", "image"]  # Include 'image' as it's part of the model
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Service Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),  # For image upload
        }


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["name", "email", "phone", "service", "details"]  # Align with the model
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone Number"}),
            "service": forms.Select(attrs={"class": "form-control"}),  # Dropdown for selecting service
            "details": forms.Textarea(attrs={"class": "form-control", "placeholder": "Details about your request"}),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "code",
            "description",
            "is_Percentage",
            "discount_value",
            "active",
            "valid_from",
            "valid_until",
            "is_onece_peruser",
        ]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Coupon Code"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Description"}),
            "is_Percentage": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "discount_value": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Discount Value"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "valid_from": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "valid_until": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "is_onece_peruser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "customer",
            "address1",
            "address2",
            "city",
            "state",
            "pincode",
            "address_type",
            "is_default",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "address1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 1"}),
            "address2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 2"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pincode"}),
            "address_type": forms.Select(attrs={"class": "form-control"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class CartTotalForm(forms.ModelForm):
    class Meta:
        model = CartTotal
        fields = ["item_total", "total", "offer", "delivery", "customer"]
        widgets = {
            "item_total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Item Total"}),
            "total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total"}),
            "offer": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Offer"}),
            "delivery": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Delivery Charge"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["customer", "product", "quantity", "option", "amount"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Quantity"}),
            "option": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Amount"}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer",
            "address",
            "order_id",
            "items",
            "sub_total",
            "delivery_charge",
            "offer",
            "total",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "order_status",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "address": forms.Select(attrs={"class": "form-control"}),
            "order_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "Order ID"}),
            "items": forms.SelectMultiple(attrs={"class": "form-control"}),
            "sub_total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Sub Total"}),
            "delivery_charge": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Delivery Charge"}),
            "offer": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Offer"}),
            "total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone_number": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "order_status": forms.Select(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["product", "user", "rating", "comment"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Rating (1-5)"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "placeholder": "Write your review here..."}),
        }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",  # For the password field from UserCreationForm
            "password2",  # For password confirmation
            "is_manager",
            "is_customer",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "is_manager": forms.CheckboxInput(attrs={"class": "form-check-input nono"}),
            "is_customer": forms.CheckboxInput(attrs={"class": "form-check-input nono"}),
        }



class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ["name", "image", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL"}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["name", "image", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL"}),
        }


class OffersForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ["name", "image1", "url1", "image2", "url2", "image3", "url3"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "image1": forms.FileInput(attrs={"class": "form-control"}),
            "url1": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL1"}),
            "image2": forms.FileInput(attrs={"class": "form-control"}),
            "url2": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL2"}),
            "image3": forms.FileInput(attrs={"class": "form-control"}),
            "url3": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL3"}),
        }
