from django import forms
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
            "delivery_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Delivery Title"}),
            "delivery_duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Delivery Duration"}),
            "garantee_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guarantee Title"}),
            "garantee_time": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guarantee Time"}),
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
            "variant": forms.Select(attrs={"class": "form-control"}),
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
        fields = ["customer", "product", "added_on"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "added_on": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Service Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
        }

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["service", "customer", "status", "requested_on"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
            "status": forms.TextInput(attrs={"class": "form-control", "placeholder": "Status"}),
            "requested_on": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["code", "discount", "expiry_date"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Coupon Code"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Discount"}),
            "expiry_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["customer", "street", "city", "state", "zip_code"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street Address"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "ZIP Code"}),
        }

class CartTotalForm(forms.ModelForm):
    class Meta:
        model = CartTotal
        fields = ["cart", "total_price"]
        widgets = {
            "cart": forms.Select(attrs={"class": "form-control"}),
            "total_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total Price"}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity", "price"]
        widgets = {
            "order": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Quantity"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "order_date", "status", "total"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "order_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "status": forms.TextInput(attrs={"class": "form-control", "placeholder": "Status"}),
            "total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total"}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["product", "customer", "rating", "review_text"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Rating"}),
            "review_text": forms.Textarea(attrs={"class": "form-control", "placeholder": "Review Text"}),
        }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "phone_number", "is_manager", "is_customer"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "is_manager": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_customer": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class OTPVerifierForm(forms.ModelForm):
    class Meta:
        model = OTPVerifier
        fields = ["user", "email", "otp"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "otp": forms.NumberInput(attrs={"class": "form-control", "placeholder": "OTP"}),
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
