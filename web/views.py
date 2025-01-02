import random
import logging
import pprint
import uuid
from django.db.models import Q
from datetime import timedelta
from django.db import IntegrityError
from django.utils import timezone
from django.utils.timezone import now
from decimal import Decimal
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import render, reverse, redirect
from collections import defaultdict
from django.http import JsonResponse,Http404,HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from promos.models import *
from items.models import *
from users.models import *
from customers.models import *

# --------------------------------------------------------------------------------------------------------------------------------

from django.db.models import Sum

def index(request):
    slider = Slider.objects.all()
    category = Category.objects.all()
    brands = Brand.objects.all()
    offer = Offer.objects.all()
    insatnces = Product.objects.all()[:10]

    # Use a different name for the annotation
    best_selling_products = (
        Product.objects.annotate(sales_count_annotation=Sum('orderitem__quantity'))
        .order_by('-sales_count_annotation')[:10]
    )

    try:
        # Assuming you want to get the latest offer
        offers = Offers.objects.latest('id')
    except Offers.DoesNotExist:
        offers = None  # Handle the case when no offers exist

    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        "slider": slider,
        "category": category,
        "offer": offer,
        "offers": offers,
        "brands": brands,
        "insatnces": insatnces,
        "best_selling_products": best_selling_products,
        "cart_count": cart_count,
    }
    return render(request, 'web/index.html', context=context)


# --------------------------------------------------------------------------------------------------------------------------------

def cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    
    # Convert total_price to Decimal
    total_price = Decimal(sum(Decimal(item.total_price()) for item in cart_items))
    delivery_charge = Decimal("0.00")  # Use Decimal for monetary values
    discount_amount = Decimal("0.00")
    best_offer = None

    if request.method == 'POST':
        code = request.POST.get('code')
        print(f"[DEBUG] Received coupon code: {code}")
        
        try:
            offer = Coupon.objects.get(code=code)
            print(f"[DEBUG] Found offer: {offer}")
            
            if not offer.is_valid():
                messages.error(request, f"Coupon '{code}' is invalid or has expired.")
            else:
                if offer.is_Percentage:
                    discount = (offer.discount_value / Decimal("100")) * total_price
                else:
                    discount = offer.discount_value
                
                if discount > discount_amount:
                    discount_amount = discount
                    best_offer = offer
                    messages.success(request, f"Coupon '{code}' applied successfully!")
                else:
                    messages.error(request, f"Coupon '{code}' does not provide a better discount.")
        except Coupon.DoesNotExist:
            print(f"[ERROR] Coupon with code '{code}' does not exist.")
            messages.error(request, f"Coupon '{code}' is invalid or has expired.")

    total_amount_to_pay = total_price + delivery_charge - discount_amount

    cart_total, created = CartTotal.objects.get_or_create(
        customer=customer,
        defaults={
            'item_total': total_price,
            'total': total_amount_to_pay,
            'offer': discount_amount,
            'delivery': delivery_charge
        }
    )

    if not created:
        cart_total.item_total = total_price
        cart_total.total = total_amount_to_pay
        cart_total.offer = discount_amount
        cart_total.delivery = delivery_charge
        cart_total.save()


    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        "cart_count": cart_count,
        "cart_count":cart_count,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_amount_to_pay": total_amount_to_pay,
        "discount_amount": discount_amount,
        "delivery_charge": delivery_charge,
        "best_offer": best_offer,
    }

    return render(request, 'web/cart.html', context=context)

# --------------------------------------------------------------------------------------------------------------------------------

# def add_to_cart(request, id):
#     product = get_object_or_404(Product, id=id)
#     user = request.user
#     customer = get_object_or_404(Customer, user=user)

#     # Check if an option is provided in the POST data
#     option_id = request.POST.get('option_id')
#     option = None
#     print(f"Received option_id: {option_id}")

#     if option_id:
#         try:
#             option = Option.objects.get(id=option_id)
#             if option.product != product:
#                 messages.error(request, "Invalid option for the selected product.")
#                 return HttpResponseRedirect(reverse("web:product_detail", args=[product.id]))
#         except Option.DoesNotExist:
#             messages.error(request, "Option does not exist.")
#             return HttpResponseRedirect(reverse("web:product_detail", args=[product.id]))

#     # Fetch quantity if provided, default to 1
#     quantity = request.POST.get('quantity', 1)

#     # Create or update the CartItem instance
#     cart_item, created = CartItem.objects.get_or_create(
#         customer=customer,
#         product=product,
#         option=option,
#         defaults={
#             "quantity": quantity,
#             "price": product.sale_price,
#         }
#     )

#     if not created:
#         cart_item.quantity += int(quantity)
#         cart_item.save()


#     messages.success(request, "Product added to cart successfully.")
#     return HttpResponseRedirect(reverse("web:cart"))



def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You need to log in to add items to the cart.")
            return redirect("web:login")

        # Retrieve customer
        customer = get_object_or_404(Customer, user=user)

        # Retrieve product details
        product_id = request.POST.get("product_id")
        color_id = request.POST.get("color_id")
        storage_value = request.POST.get("storage_value")
        ram_value = request.POST.get("ram_value")
        
        product = get_object_or_404(Product, id=product_id)
        option = None
        
        # Check if options are provided and match an existing variant
        if color_id or storage_value or ram_value:
            option = Option.objects.filter(
                product=product,
                color_id=color_id,
                storage=storage_value,
                ram=ram_value,
            ).first()
            if not option:
                messages.error(request, "The selected product option is unavailable.")
                return redirect("web:product", id=product.id)
        
        # Determine price
        price = option.sale_price if option else product.sale_price

        # Check if the item already exists in the cart
        existing_item = CartItem.objects.filter(
            customer=customer, product=product, option=option
        ).first()

        if existing_item:
            # Update quantity if item already exists
            existing_item.quantity += 1
            existing_item.save()
            messages.success(request, "Cart updated with the selected item.")
        else:
            # Add new cart item
            CartItem.objects.create(
                customer=customer,
                product=product,
                option=option,
                quantity=1,
                price=price,
            )
            messages.success(request, "Item added to your cart.")

        # Redirect to the cart or stay on the product page
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Item added to cart"})
        
        return redirect("web:product", id=product.id)
    else:
        return redirect("web:index")



# --------------------------------------------------------------------------------------------------------------------------------


def cart_plus(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    cart_item = CartItem.objects.get(id=id, customer=customer)

    cart_item.quantity += 1
    cart_item.price += cart_item.product.sale_price
    cart_item.save()
    
    return HttpResponseRedirect(reverse("web:cart"))

# --------------------------------------------------------------------------------------------------------------------------------

def cart_minus(request, id):
    
    user = request.user
    customer = Customer.objects.get(user=user)
    cart_item = CartItem.objects.get(id=id, customer=customer)

    cart_item.quantity -= 1
    cart_item.price -= cart_item.product.sale_price
    cart_item.save()

    if cart_item.quantity == 0:
        cart_item.delete()
    
    return HttpResponseRedirect(reverse("web:cart"))

# --------------------------------------------------------------------------------------------------------------------------------

def login(request):

    if request.user.is_authenticated:
        return redirect(reverse("web:index"))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            return redirect(reverse("web:index"))  # Redirect to the index page or any desired page
        else:
            # Show an error if authentication fails
            context = {
                "title": "title",
                "error": True,
                "message": "Invalid email or password"
            }
            return render(request, "web/login.html", context=context)

    else:
        context = {
            "title": "title",
        }
        return render(request, "web/login.html", context=context)
    
# --------------------------------------------------------------------------------------------------------------------------------

# def register(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number', None)  # Default to None if not provided
#         password = request.POST.get('password')

#         # If phone number is an empty string, set it to None (this handles the uniqueness constraint)
#         if phone_number == '':
#             phone_number = None

#         # Check if email already exists
#         if User.objects.filter(email=email,phone_number=phone_number).exists():
#             # Display an error message if email is already registered
#             context = {
#                 "error": True,
#                 "message": "This email is already registered. Please log in or use a different email."
#             }
#             return render(request, "web/signup.html", context=context)
            
        
#         else:
#             user = User.objects.get(email=email)  # Retrieve existing user by email
            
#             # Check if OTPVerifier exists for the user and delete previous OTP if any
#             if OTPVerifier.objects.filter(user=user).exists():
#                 otp_verifier = OTPVerifier.objects.get(user=user)
#                 otp_verifier.delete()
                
#                 otp = random.randrange(1000, 9999)  # Generate new OTP
#                 otp_verifier = OTPVerifier.objects.create(user=user, otp=otp)  # Create OTP record
#                 otp_verifier.save()

#                 # Send OTP email
#                 subject = 'Your OTP for register'
#                 message = f'Your OTP is: {otp}'
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [user.email]

#                 # send_mail(subject, message, email_from, recipient_list)
#                 print(message)  # Just printing for now, use send_mail in production

#                 # Redirect to OTP verification page
#                 return HttpResponseRedirect(reverse("web:verify_register", kwargs={'email': email}))

#             # Create new user if email doesn't exist
#             user = User.objects.create_user(
#                 email=email,
#                 password=password,
#                 first_name=first_name,
#                 last_name=last_name,
#                 phone_number=phone_number,  # Can be None if not provided
#                 is_customer=True
#             )

#             user.save()

#             # Create customer object associated with the user
#             customer = Customer.objects.create(
#                 user=user
#             )
#             customer.save()

#             # Generate OTP for the new user
#             otp = random.randrange(1000, 9999)
#             otp_verifier = OTPVerifier.objects.create(user=user, otp=otp)
#             otp_verifier.save()

#             # Send OTP email
#             subject = 'Your OTP for register'
#             message = f'Your OTP is: {otp}'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]

#             # send_mail(subject, message, email_from, recipient_list)
#             print(otp)  # Just printing for now, use send_mail in production

#             # Redirect to OTP verification page
#             return HttpResponseRedirect(reverse("web:verify_register", kwargs={'email': email}))

#     else:
#         context = {
#             "title": "register",
#         }
#         return render(request, "web/signup.html", context=context)
    



def register(request):

    if request.user.is_authenticated:
        return redirect(reverse("web:index"))


    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number', '').strip() or None
        password = request.POST.get('password')

        # Check if email or phone number already exists
        if User.objects.filter(email=email).exists():
            context = {
                "error": True,
                "message": "This email is already registered. Please log in or use a different email."
            }
            return render(request, "web/signup.html", context=context)

        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            context = {
                "errorp": True,
                "message": "This phone number is already registered. Please use a different phone number."
            }
            return render(request, "web/signup.html", context=context)

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Store OTP in the OTPVerifier model without a user
        OTPVerifier.objects.create(
            otp=otp,
            user=None,  # Temporarily not assigning a user
            email=email,
        )

        # Store registration data in the session
        request.session['registration_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'password': password,
        }

        # Send OTP email
        subject = 'Your OTP for registration'
        message = f'Your OTP is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]

        # Uncomment in production
        # send_mail(subject, message, email_from, recipient_list)
        print(f"Generated OTP: {otp}")  # Debugging purposes

        # Redirect to OTP verification page
        return HttpResponseRedirect(reverse("web:verify_register", kwargs={'email': email}))

    return render(request, "web/signup.html", {"title": "Register"})

# --------------------------------------------------------------------------------------------------------------------------------

def verify_register(request, email):
    try:
        # Get the latest OTPVerifier record associated with this email
        otp_verifier = OTPVerifier.objects.filter(email=email).last()

        if not otp_verifier:
            return HttpResponse("OTP record not found. Please register again.")

        # Check if OTP has expired (example: 5 minutes validity)
        otp_expiry_time = otp_verifier.created_datetime + timedelta(minutes=5)
        if now() > otp_expiry_time:
            otp_verifier.delete()  # Clean up expired OTP record
            return HttpResponse("OTP has expired. Please register again.")
    except User.DoesNotExist:
        return HttpResponse("User not found")

    if request.method == "POST":
        otp = request.POST.get('otp')
        if str(otp_verifier.otp) == otp:
            # OTP is correct, activate the user
            user = otp_verifier.user
            if not user:
                # User creation was deferred; retrieve session data
                registration_data = request.session.get('registration_data')
                if not registration_data:
                    return HttpResponse("Session expired. Please register again.")

                user = User.objects.create_user(
                    email=registration_data['email'],
                    password=registration_data['password'],
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    phone_number=registration_data['phone_number'],
                    is_customer=True,
                )
                customer = Customer.objects.create(
                user=user
                )
                customer.save()
                otp_verifier.user = user
                otp_verifier.save()

            # Log in the user
            auth_login(request, user)

            # Clean up OTP record
            otp_verifier.delete()
            return HttpResponseRedirect(reverse("web:login"))
        else:
            context = {
                "title": "OTP Verification",
                "error": True,
                "message": "Invalid OTP. Please try again.",
            }
            return render(request, "web/verify.html", context=context)

    return render(request, "web/verify.html", {"title": "OTP Verification", "email": email})

# --------------------------------------------------------------------------------------------------------------------------------

def resend_otp(request, email):
    try:
        # Fetch or create an OTPVerifier record by email
        otp = random.randint(100000, 999999)

        otp_verifier, created = OTPVerifier.objects.update_or_create(
            email=email,
            defaults={'otp': otp, 'created_datetime': now()}
        )

        # Send OTP email
        subject = 'Your OTP for registration'
        message = f'Your new OTP is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]

        # Uncomment to send email in production
        # send_mail(subject, message, email_from, recipient_list)
        print(f"Resent OTP: {otp}")  # Debugging purposes

        return JsonResponse({'success': True, 'message': 'OTP resent successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



    
# --------------------------------------------------------------------------------------------------------------------------------

def user_logout(request):
    logout(request)
    return redirect('web:index') 

# --------------------------------------------------------------------------------------------------------------------------------

# def checkout(request):
#     customer = get_object_or_404(Customer, user=request.user)
#     cart_items = CartItem.objects.filter(customer=customer)
#     addresses = Address.objects.filter(customer=customer)
#     total_price = Decimal(sum(item.total_price() for item in cart_items))
#     delivery_charge = Decimal("50.00")  # Example delivery charge
#     discount_amount = Decimal("0.00")
#     best_offer = None

#     if not cart_items:
#         messages.error(request, "Your cart is empty. Please add items to proceed to checkout.")
#         return redirect('cart')

#     if request.method == 'POST':
#         # Fetch the form data
#         address_id = request.POST.get('address')
#         coupon_code = request.POST.get('coupon')

#         # Validate address
#         address = get_object_or_404(Address, id=address_id, customer=customer)

#         # Apply coupon if available
#         if coupon_code:
#             try:
#                 offer = Coupon.objects.get(code=coupon_code)
#                 if offer.is_valid():
#                     if offer.is_Percentage:
#                         discount_amount = (offer.discount_value / Decimal("100")) * total_price
#                     else:
#                         discount_amount = offer.discount_value
#                     best_offer = offer
#                 else:
#                     messages.error(request, "The coupon is invalid or expired.")
#             except Coupon.DoesNotExist:
#                 messages.error(request, "The coupon code is invalid.")

#         # Calculate total
#         total_amount = total_price + delivery_charge - discount_amount

#         # Create Order
#         order = Order.objects.create(
#             customer=customer,
#             address=address,
#             order_id=str(uuid.uuid4()),
#             sub_total=float(total_price),
#             delivery_charge=float(delivery_charge),
#             total=float(total_amount),
#             first_name=request.POST.get('first_name'),
#             last_name=request.POST.get('last_name'),
#             email=request.POST.get('email'),
#             phone_number=request.POST.get('phone_number'),
#             order_status='IN',  # Initiated status
#         )
#         for item in cart_items:
#             order_item = OrderItem.objects.create(
#                 customer=customer,
#                 product=item.product,
#                 quantity=item.quantity,
#                 option=item.option,
#                 amount=item.total_price(),
#             )
#             order.items.add(order_item)
#         order.save()

#         # Clear cart
#         cart_items.delete()

#         messages.success(request, "Your order has been placed successfully!")
#         return redirect('order_summary', order_id=order.order_id)

#     context = {
#         "cart_items": cart_items,
#         "addresses": addresses,
#         "total_price": total_price,
#         "delivery_charge": delivery_charge,
#         "discount_amount": discount_amount,
#         "total_amount": total_price + delivery_charge - discount_amount,
#     }
#     return render(request, 'web/checkout.html', context)


def checkout(request):
    customer = Customer.objects.get(user=request.user)
    addresses = Address.objects.filter(customer=customer)
    cart_items = CartItem.objects.filter(customer=customer)
    cart_bill = CartTotal.objects.get(customer=customer)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        # Get the selected address
        address = Address.objects.get(id=address_id, customer=customer)

        # Create order
        order = Order.objects.create(
            customer=customer,
            address=address,
            order_id=f"ORD{Order.objects.count() + 1}",
            sub_total=cart_bill.item_total,
            total=cart_bill.total,
            offer=cart_bill.offer,            
            delivery_charge=cart_bill.delivery,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            order_status="IN",
        )
        
        # Add cart items to order and link them
        for item in cart_items:
            order_item = OrderItem.objects.create(
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                amount=item.price,
                option=item.option,
            )
            order.items.add(order_item)  # Link the OrderItem to the Order
        
        # Clear cart after checkout
        cart_items.delete()

        return redirect("web:index")  # Redirect to a success page

    return render(request, "web/checkout.html", {
        "addresses": addresses,
        "cart_items": cart_items,
        'subtotal': cart_bill.item_total or 0,
        'discount': cart_bill.offer or 0,
        'delivery': cart_bill.delivery if cart_bill else 0,
        'total': cart_bill.total if cart_bill else 0,
    })

# --------------------------------------------------------------------------------------------------------------------------------

def category(request,id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    category_all =Category.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    context ={
        "cart_count": cart_count,
        'products': products,
        'category': category,
        'category_all': category_all,

    }
    return render(request, 'web/category.html',context=context)

# --------------------------------------------------------------------------------------------------------------------------------

def brand(request, id):
    # Fetch the specific brand
    brand = get_object_or_404(Brand, id=id)
    # Fetch products for the specific brand
    products = Product.objects.filter(brand=brand)
    # Fetch all brands for the carousel
    brand_all = Brand.objects.all()

    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        "cart_count": cart_count,
        'products': products,
        'brand': brand,
        'brand_all': brand_all,
    }
    return render(request, 'web/brand.html', context=context)

# --------------------------------------------------------------------------------------------------------------------------------

def order(request, id):
    customer = get_object_or_404(Customer, user=request.user)
    try:
        # Ensure the order belongs to the logged-in customer
        order = Order.objects.get(id=id, customer=customer)
    except Order.DoesNotExist:
        raise Http404("Order not found or does not belong to you.")
    
    context = {
        'order': order,
        'items': order.items.all()  # Retrieve associated order items
    }
    return render(request,'web/order.html',context=context)

# --------------------------------------------------------------------------------------------------------------------------------

def orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.prefetch_related('items__product').select_related('customer', 'address').all()
    
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        "cart_count": cart_count,
        'orders': orders,
    }
    return render(request, 'web/orders.html', context=context)


# --------------------------------------------------------------------------------------------------------------------------------

def product(request, id):
    product = get_object_or_404(Product, id=id)
    user = request.user
    customer = get_object_or_404(Customer, user=user)
    specs = Spec.objects.filter(product=product).select_related('image')
    is_in_cart = CartItem.objects.filter(customer=customer, product=product).exists()
    related_products = Product.objects.filter(
        Q(category=product.category) & ~Q(id=product.id)
    )[:10]
    reviews = product.reviews.all()


    options = Option.objects.filter(product=product).select_related("color")
    specifications = product.specifications.all()

    # Retrieve selected options
    selected_color_id = request.GET.get("color_id")
    selected_storage_value = request.GET.get("storage_value")
    selected_ram_value = request.GET.get("ram_value")

    # Defaults
    first_option = options.first() if options.exists() else None
    selected_color_id = selected_color_id or (first_option.color.id if first_option and first_option.color else None)
    selected_storage_value = selected_storage_value or (first_option.storage if first_option else None)
    selected_ram_value = selected_ram_value or (first_option.ram if first_option else None)

    # Find matching option
    matching_option = options.filter(
        color_id=selected_color_id,
        storage=selected_storage_value,
        ram=selected_ram_value,
    ).first()

    # Group options by storage and RAM
    grouped_options = defaultdict(lambda: defaultdict(set))
    for option in options:
        grouped_options[option.storage][option.ram].add(option.color)

    grouped_options = {
        storage: {ram: list(colors) for ram, colors in rams.items()}
        for storage, rams in grouped_options.items()
    }

    # Filtered Colors
    filtered_colors = set()
    if selected_storage_value and selected_ram_value:
        filtered_colors = {
            option.color for option in options
            if option.storage == selected_storage_value and option.ram == selected_ram_value
        }

    unique_colors = list(filtered_colors)
    unique_storages = {option.storage for option in options}
    unique_rams = {option.ram for option in options}

    ram_options_for_selected_storage = grouped_options.get(selected_storage_value, {})

    # Images and Price
    selected_images = matching_option.images.all() if matching_option else []
    selected_price = matching_option.sale_price if matching_option else product.sale_price

    wishlist_items = Whishlist.objects.filter(customer=customer).values_list('product', flat=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response_data = {
            "main_image_url": selected_images[0].image.url if selected_images else "",
            "thumbnails": [
                {"image_url": image.image.url, "alt_text": image.alt_text}
                for image in selected_images
            ],
            "product_name": product.name,
            "price": selected_price,
            "selected_color_id": selected_color_id,
            "selected_storage_value": selected_storage_value,
            "selected_ram_value": selected_ram_value,
        }
        return JsonResponse(response_data)




    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        "reviews": reviews,
        "related_products": related_products,
        "cart_count": cart_count,
        "specs": specs,
        "ram_options_for_selected_storage": ram_options_for_selected_storage,
        "wishlist_items": wishlist_items,
        "product": product,
        "specifications": specifications,
        "grouped_options": grouped_options,
        "unique_colors": unique_colors,
        "unique_storages": list(unique_storages),
        "unique_rams": list(unique_rams),
        "selected_images": selected_images,
        "selected_price": selected_price,
        "selected_color_id": selected_color_id,
        "selected_storage_value": selected_storage_value,
        "selected_ram_value": selected_ram_value,
        "is_in_cart": is_in_cart,
    }

    return render(request, 'web/product.html', context=context)

# --------------------------------------------------------------------------------------------------------------------------------

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the user has purchased the product
    has_ordered = Order.objects.filter(user=request.user, product=product).exists()
    if not has_ordered:
        messages.error(request, "You can only review products you have purchased.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']

        # Ensure the user hasn't already reviewed the product
        existing_review = Review.objects.filter(product=product, user=request.user).exists()
        if existing_review:
            messages.error(request, "You have already reviewed this product.")
            return redirect('product_detail', product_id=product.id)

        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, "Review added successfully!")
        return redirect('product_detail', product_id=product.id)

    return render(request, 'web/add_review.html', {'product': product})

# --------------------------------------------------------------------------------------------------------------------------------

def whishlist(request):
    customer = Customer.objects.get(user=request.user)
    wishlist_items = Whishlist.objects.filter(customer=customer)
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    return render(request, 'web/whishlist.html', {"cart_count": cart_count,'wishlist_items': wishlist_items})

# --------------------------------------------------------------------------------------------------------------------------------

def add_to_wishlist(request, id):
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, id=id)
    
    
    if Whishlist.objects.filter(customer=customer, product=product).exists():
        return JsonResponse({'message': 'Product already in wishlist'}, status=400)

   
    Whishlist.objects.create(customer=customer, product=product)
    return HttpResponseRedirect(reverse("web:product",kwargs={'id': product.id}))

# --------------------------------------------------------------------------------------------------------------------------------

def remove_from_wishlist(request, id):
    """Remove a product from the wishlist."""
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, id=id)
    
    # Remove the product from the wishlist if it exists
    wishlist_item = Whishlist.objects.filter(customer=customer, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
    # Determine the previous page from the "Referer" header
    referer = request.META.get('HTTP_REFERER', '')
    if 'whishlist' in referer:
        # Redirect to wishlist page if coming from there
        return HttpResponseRedirect(reverse("web:whishlist"))
    else:
        # Default to product page
        return HttpResponseRedirect(reverse("web:product", kwargs={'id': product.id}))

# --------------------------------------------------------------------------------------------------------------------------------

def services(request):
    services = Service.objects.all()
    print(services)  # Check if services are being fetched
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    return render(request, 'web/service.html', {"cart_count": cart_count,'services': services})

# --------------------------------------------------------------------------------------------------------------------------------

def request_service(request):
    services = Service.objects.all()  # Renamed to avoid conflict with form input
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone')
        service_id = request.POST.get('service')  # Use 'service' to get the ID
        details = request.POST.get('details')
        
        try:
            service = Service.objects.get(id=service_id)  # Fetch the Service instance
        except Service.DoesNotExist:
            return HttpResponse("Invalid service selected", status=400)

        # Construct the email body
        email_body = f"""
        New Service Request:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Selected Service: {service.title}
        Details: {details}

        Please follow up with the customer at the earliest.
        """

        # Send email
        # try:
        #     send_mail(
        #         subject=f"Service Request: {service.title}",
        #         message=email_body,
        #         from_email='noreply@yourdomain.com',
        #         recipient_list=['your_email@domain.com'],  # Replace with your email address
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     return HttpResponse(f"Error sending email: {e}", status=500)

        # Log and save the request
        print(name, email, phone, service.title, details)
        ServiceRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            details=details
        )
        
        return redirect('web:service')
    
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, 'web/service.html', {"cart_count": cart_count,'services': services})

    
# --------------------------------------------------------------------------------------------------------------------------------

# def apply_coupon(request):
#     if request.method == "POST":
#         customer = get_object_or_404(Customer, user=request.user)
#         cart_items = CartItem.objects.filter(customer=customer)
        
#         # Get the coupon code from the POST request
#         coupon_code = request.POST.get("coupon")
#         total_price = sum(item.product.sale_price * item.quantity for item in cart_items)

#         try:
#             # Check if the coupon exists
#             coupon = Coupon.objects.get(code=coupon_code)

#             # Validate the coupon
#             if not coupon.is_valid():
#                 return JsonResponse({"success": False, "message": "Coupon is not valid or expired."})

#             # Calculate the discount
#             if coupon.is_Percentage:
#                 discount = total_price * (coupon.discount_value / 100)
#             else:
#                 discount = coupon.discount_value

#             # Ensure the discount doesn't exceed the total price
#             discount = min(discount, total_price)
#             discounted_total = total_price - discount

#             return JsonResponse({
#                 "success": True,
#                 "discount": round(discount, 2),
#                 "discounted_total": round(discounted_total, 2),
#                 "message": "Coupon applied successfully."
#             })

#         except Coupon.DoesNotExist:
#             return JsonResponse({"success": False, "message": "Invalid coupon code."})

#     return JsonResponse({"success": False, "message": "Invalid request method."})

# --------------------------------------------------------------------------------------------------------------------------------

def add_address(request):
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        Address.objects.create(
            customer=customer,
            address1=request.POST["address1"],
            address2=request.POST.get("address2", ""),
            city=request.POST["city"],
            state=request.POST["state"],
            pincode=request.POST["pincode"],
            address_type=request.POST["address_type"],
        )
        # Redirect based on the 'next' query parameter
        next_page = request.GET.get("next", "web:manage_addresses")
        return redirect(next_page)
    
    return render(request, "web/add_address.html")


# --------------------------------------------------------------------------------------------------------------------------------

def edit_address(request, id):
    address = get_object_or_404(Address, id=id, customer__user=request.user)
    if request.method == "POST":
        address.address1 = request.POST["address1"]
        address.address2 = request.POST.get("address2", "")
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.pincode = request.POST["pincode"]
        address.address_type = request.POST["address_type"]
        address.save()
        # Redirect based on the 'next' query parameter
        next_page = request.GET.get("next", "web:manage_addresses")
        return redirect(next_page)
    
    return render(request, "web/add_address.html", {"address": address, "is_edit": True})



# --------------------------------------------------------------------------------------------------------------------------------

def manage_addresses(request):
    customer = Customer.objects.get(user=request.user)
    addresses = Address.objects.filter(customer=customer)
    return render(request, "web/address.html", {"addresses": addresses})

# --------------------------------------------------------------------------------------------------------------------------------

def account(request):
    recent_orders = Order.objects.all()[:3]
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        "cart_count": cart_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'web/account.html', context)

# --------------------------------------------------------------------------------------------------------------------------------

def delete_address(request, id):
    address = get_object_or_404(Address, id=id, customer__user=request.user)
    address.delete()
    # Redirect based on the 'next' query parameter
    next_page = request.GET.get("next", "web:manage_addresses")
    return redirect(next_page)


# --------------------------------------------------------------------------------------------------------------------------------

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('web:reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            message = render_to_string('web/forgot_password.html', {'reset_link': reset_link})
            # send_mail(
            #     'Password Reset Request',
            #     message,
            #     'noreply@example.com',
            #     [email],
            #     fail_silently=False,
            # )
            print(reset_link)
            return render(request, 'web/forgot_password.html', {'success_message': True})
        except User.DoesNotExist:
            return render(request, 'web/forgot_password.html', {'error_message': 'No account associated with this email'})
    else:
        return render(request, 'web/forgot_password.html')
    
# --------------------------------------------------------------------------------------------------------------------------------

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST.get('password')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after reset
                return HttpResponseRedirect(reverse('web:login'))
            else:
                return render(request, 'web/reset_password.html', {'error_message': 'Invalid reset link'})
        except User.DoesNotExist:
            return render(request, 'web/reset_password.html', {'error_message': 'Invalid reset link'})
    else:
        return render(request, 'web/reset_password.html')

# --------------------------------------------------------------------------------------------------------------------------------

