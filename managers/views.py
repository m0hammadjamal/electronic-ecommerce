from django.shortcuts import render
import datetime
from django.db.models import Sum

from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_manager
from main.functions import generate_form_errors

from promos.models import *
from items.models import Category, Brand, Color, CustomSpecification, Product, Option, ProductImage,Ram, Storage, IconImage, Spec
from users.models import *
from customers.models import Customer, CartItem, Whishlist, Service,ServiceRequest, Coupon, Address, CartTotal, OrderItem, Order, Review
from managers.forms import *
from managers.models import *


@login_required(login_url="/app/login")
@allow_manager
def index(request):    
    orders = Order.objects.all().exclude(order_status='IN').count()
    earnings = Order.objects.exclude(order_status__in=['IN', 'CA']).aggregate(Sum('total'))["total__sum"]
    items = Product.objects.all().count()
    customers = Customer.objects.all().count()

    instances = Order.objects.all().exclude(order_status='IN')[:5]
    
    context= {
        "title": "Store | Dashboard",
        "items": items,
        "customers": customers,
        "earnings":earnings,
        "orders": orders,
        "instances":instances
    }
    return render(request, "panel/index.html", context=context)



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_manager:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("managers:index"))
            else:
                context= {
                    "title": "Manager Login | Home",
                    "error": True,
                    "message": "Invalid credentials"
                }
                return render(request, "panel/login.html", context=context)
        else:
            context= {
                "title": "Manager Login | Home",
                "error": True,
                "message": "Invalid credentials"
            }
            return render(request, "panel/login.html", context=context)
    else:
        context= {
            "title" : "Manager Login | Home"
        }
        return render(request, "panel/login.html", context=context)



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("managers:login"))


@login_required(login_url="/app/login")
@allow_manager
def order(request,id):
    user = request.user
    manager = Manager.objects.get(user=user)
    
    instance = get_object_or_404(Order, id=id)

    
    context= {
        "title": "Orders | Dashboard",
        "sub_title": "Orders",
        "name": "Orders List",
        "instance":instance,
    }
    return render(request, "panel/order.html", context=context)



@login_required(login_url="/app/login")
@allow_manager
def reports(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    
    instances = Order.objects.all().exclude(order_status__in=['IN', 'CA'])

    
    context= {
        "title": "Reports | Dashboard",
        "sub_title": "Reports",
        "name": "Reports List",
        "instances":instances,
    }
    return render(request, "panel/reports.html", context=context)




@login_required(login_url="/app/login")
@allow_manager
def settings(request):
    user = request.user
    manager = Manager.objects.get(user=user)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Update user details
        user.first_name = first_name
        user.last_name = last_name

        # Update phone_number only if it's provided
        if phone_number:
            user.phone_number = phone_number
        else:
            user.phone_number = None  # Clear phone number if no input

        user.save()

        return HttpResponseRedirect(reverse('managers:settings'))
    else:
        context = {
            "title": "Settings | Dashboard",
            "sub_title": "Settings",
            "name": "Settings",
            "manager": manager,
        }
        return render(request, "panel/settings.html", context=context)
    

@login_required(login_url="/app/login")
@allow_manager
def password(request):
    user = request.user
    manager = Manager.objects.get(user=user)

    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password!= password2:
            context= {
                "title": "Settings | Dashboard",
                "sub_title": "Settings",
                "error": True,
                "message": "Password is missmatch",
                "name": "Settings",
                "manager":manager,
            }
            return render(request, "panel/password.html", context=context)
        
        else:
            user.set_password(password)
            user.save()

            return HttpResponseRedirect(reverse('managers:settings'))
    else:

        context= {
            "title": "Settings | Dashboard",
            "sub_title": "Settings",
            "name": "Settings",
            "manager":manager,
        }
        return render(request, "panel/password.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def customer_order(request,id):
    user = request.user
    manager = Manager.objects.get(user=user)

    customer = Customer.objects.get(id=id)
    
    instances = Order.objects.filter(customer=customer).exclude(order_status='IN')

    
    context= {
        "title": "Custoemr | Dashboard",
        "sub_title": "Custoemr",
        "name": "Orders List",
        "instances":instances,
    }
    return render(request, "panel/orders.html", context=context)




@login_required(login_url="/app/login")
@allow_manager
def order_accept(request,id):

    instance = get_object_or_404(Order, id=id)

    instance.order_status = 'IP'
    instance.save()

    return HttpResponseRedirect(reverse("managers:order", kwargs={'id': instance.id}))


@login_required(login_url="/app/login")
@allow_manager
def order_reject(request,id):

    instance = get_object_or_404(Order, id=id)

    instance.order_status = 'CA'
    instance.save()

    return HttpResponseRedirect(reverse("managers:order", kwargs={'id': instance.id}))


@login_required(login_url="/app/login")
@allow_manager
def order_dispatched(request,id):

    instance = get_object_or_404(Order, id=id)

    instance.order_status = 'DI'
    instance.save()

    return HttpResponseRedirect(reverse("managers:order", kwargs={'id': instance.id}))


@login_required(login_url="/app/login")
@allow_manager
def order_completed(request,id):

    instance = get_object_or_404(Order, id=id)

    instance.order_status = 'CO'
    instance.save()

    return HttpResponseRedirect(reverse("managers:order", kwargs={'id': instance.id}))


@login_required(login_url="/app/login")
@allow_manager
def categories(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Category.objects.all().order_by('-id')
    context = {
        "title": "Categories | Dashboard",
        "sub_title": "Categories",
        "name": "Categories List",
        "instances": instances,
    }
    return render(request, "panel/categories.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def categories_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:categories"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Category",
                "sub_title": "Categories",
                "name": "Add Category",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/categories-add.html", context=context)

    form = CategoryForm()
    context = {
        "title": "Manager Dashboard | Add Category",
        "sub_title": "Categories",
        "name": "Add Category",
        "form": form,
    }
    return render(request, "panel/categories-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def categories_edit(request, id):
    instance = Category.objects.get(id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:categories"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Category",
                "sub_title": "Categories",
                "name": "Edit Category",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/categories-add.html", context=context)

    form = CategoryForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Category",
        "sub_title": "Categories",
        "name": "Edit Category",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/categories-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def categories_delete(request, id):
    instance = Category.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:categories"))


@login_required(login_url="/app/login")
@allow_manager
def brands(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Brand.objects.all().order_by('-id')
    context = {
        "title": "Brands | Dashboard",
        "sub_title": "Brands",
        "name": "Brands List",
        "instances": instances,
    }
    return render(request, "panel/brands.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def brands_add(request):
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:brands"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Brand",
                "sub_title": "Brands",
                "name": "Add Brand",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/brands-add.html", context=context)

    form = BrandForm()
    context = {
        "title": "Manager Dashboard | Add Brand",
        "sub_title": "Brands",
        "name": "Add Brand",
        "form": form,
    }
    return render(request, "panel/brands-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def brands_edit(request, id):
    instance = Brand.objects.get(id=id)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:brands"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Brand",
                "sub_title": "Brands",
                "name": "Edit Brand",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/brands-add.html", context=context)

    form = BrandForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Brand",
        "sub_title": "Brands",
        "name": "Edit Brand",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/brands-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def brands_delete(request, id):
    instance = Brand.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:brands"))


@login_required(login_url="/app/login")
@allow_manager
def colors(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Color.objects.all()
    context = {
        "title": "Colors | Dashboard",
        "sub_title": "Colors",
        "name": "Colors List",
        "instances": instances,
    }
    return render(request, "panel/colors.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def colors_add(request):
    if request.method == "POST":
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:colors"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Color",
                "sub_title": "Colors",
                "name": "Add Color",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/colors-add.html", context=context)

    form = ColorForm()
    context = {
        "title": "Manager Dashboard | Add Color",
        "sub_title": "Colors",
        "name": "Add Color",
        "form": form,
    }
    return render(request, "panel/colors-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def colors_edit(request, id):
    instance = Color.objects.get(id=id)
    if request.method == "POST":
        form = ColorForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:colors"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Color",
                "sub_title": "Colors",
                "name": "Edit Color",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/colors-add.html", context=context)

    form = ColorForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Color",
        "sub_title": "Colors",
        "name": "Edit Color",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/colors-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def colors_delete(request, id):
    instance = Color.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:colors"))


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = CustomSpecification.objects.all().order_by('-id')
    context = {
        "title": "Custom Specifications | Dashboard",
        "sub_title": "Custom Specifications",
        "name": "Custom Specifications List",
        "instances": instances,
    }
    return render(request, "panel/custom-specifications.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications_add(request):
    if request.method == "POST":
        form = CustomSpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:custom_specifications"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Custom Specification",
                "sub_title": "Custom Specifications",
                "name": "Add Custom Specification",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/custom-specifications-add.html", context=context)

    form = CustomSpecificationForm()
    context = {
        "title": "Manager Dashboard | Add Custom Specification",
        "sub_title": "Custom Specifications",
        "name": "Add Custom Specification",
        "form": form,
    }
    return render(request, "panel/custom-specifications-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications_edit(request, id):
    instance = CustomSpecification.objects.get(id=id)
    if request.method == "POST":
        form = CustomSpecificationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:custom_specifications"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Custom Specification",
                "sub_title": "Custom Specifications",
                "name": "Edit Custom Specification",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/custom-specifications-add.html", context=context)

    form = CustomSpecificationForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Custom Specification",
        "sub_title": "Custom Specifications",
        "name": "Edit Custom Specification",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/custom-specifications-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications_delete(request, id):
    instance = CustomSpecification.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:custom_specifications"))


@login_required(login_url="/app/login")
@allow_manager
def options(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Option.objects.all().order_by('-id')
    context = {
        "title": "Options | Dashboard",
        "sub_title": "Options",
        "name": "Options List",
        "instances": instances,
    }
    return render(request, "panel/options.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def options_add(request):
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:options"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Option",
                "sub_title": "Options",
                "name": "Add Option",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/options-add.html", context=context)

    form = OptionForm()
    context = {
        "title": "Manager Dashboard | Add Option",
        "sub_title": "Options",
        "name": "Add Option",
        "form": form,
    }
    return render(request, "panel/options-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def options_edit(request, id):
    instance = Option.objects.get(id=id)
    if request.method == "POST":
        form = OptionForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:options"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Option",
                "sub_title": "Options",
                "name": "Edit Option",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/options-add.html", context=context)

    form = OptionForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Option",
        "sub_title": "Options",
        "name": "Edit Option",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/options-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def options_delete(request, id):
    instance = Option.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:options"))



@login_required(login_url="/app/login")
@allow_manager
def product_images(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = ProductImage.objects.all().order_by('-id')
    context = {
        "title": "Product Images | Dashboard",
        "sub_title": "Product Images",
        "name": "Product Images List",
        "instances": instances,
    }
    return render(request, "panel/product-images.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def product_images_add(request):
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:product_images"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Product Image",
                "sub_title": "Product Images",
                "name": "Add Product Image",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/product-images-add.html", context=context)

    form = ProductImageForm()
    context = {
        "title": "Manager Dashboard | Add Product Image",
        "sub_title": "Product Images",
        "name": "Add Product Image",
        "form": form,
    }
    return render(request, "panel/product-images-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def product_images_edit(request, id):
    instance = ProductImage.objects.get(id=id)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:product_images"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Product Image",
                "sub_title": "Product Images",
                "name": "Edit Product Image",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/product-images-add.html", context=context)

    form = ProductImageForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Product Image",
        "sub_title": "Product Images",
        "name": "Edit Product Image",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/product-images-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def product_images_delete(request, id):
    instance = ProductImage.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:product_images"))



@login_required(login_url="/app/login")
@allow_manager
def rams(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Ram.objects.all()
    context = {
        "title": "RAMs | Dashboard",
        "sub_title": "RAMs",
        "name": "RAMs List",
        "instances": instances,
    }
    return render(request, "panel/rams.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def rams_add(request):
    if request.method == "POST":
        form = RamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:rams"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add RAM",
                "sub_title": "RAMs",
                "name": "Add RAM",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/rams-add.html", context=context)

    form = RamForm()
    context = {
        "title": "Manager Dashboard | Add RAM",
        "sub_title": "RAMs",
        "name": "Add RAM",
        "form": form,
    }
    return render(request, "panel/rams-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def rams_edit(request, id):
    instance = Ram.objects.get(id=id)
    if request.method == "POST":
        form = RamForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:rams"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit RAM",
                "sub_title": "RAMs",
                "name": "Edit RAM",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/rams-add.html", context=context)

    form = RamForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit RAM",
        "sub_title": "RAMs",
        "name": "Edit RAM",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/rams-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def rams_delete(request, id):
    instance = Ram.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:rams"))


@login_required(login_url="/app/login")
@allow_manager
def services(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Service.objects.all()

    context = {
        "title": "Services | Dashboard",
        "sub_title": "Services",
        "name": "Services List",
        "instances": instances,
    }
    return render(request, "panel/services.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def services_add(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)  # Ensure you pass request.FILES for image upload
        if form.is_valid():
            form.save()  # Save the form data
            return HttpResponseRedirect(reverse("managers:services"))  # Redirect to the services list page after submission
        else:
            message = "There were errors in the form. Please correct them below."
    else:
        form = ServiceForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Service",
        "sub_title": "Services",
        "name": "Add Service",
        "form": form,
        "message": message,
    }
    return render(request, "panel/services-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def services_edit(request, id):
    instance = get_object_or_404(Service, id=id)  # Better than using Service.objects.get()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=instance)  # Ensure request.FILES is included for image upload
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:services"))  # Redirect after saving
        else:
            message = "There were errors in the form. Please correct them below."
    else:
        form = ServiceForm(instance=instance)  # Pre-populate form with existing instance data
        message = None

    context = {
        "title": "Manager Dashboard | Edit Service",
        "sub_title": "Services",
        "name": "Edit Service",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/services-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def services_delete(request, id):
    instance = Service.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:services"))



@login_required(login_url="/app/login")
@allow_manager
def service_requests(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = ServiceRequest.objects.all()
    context = {
        "title": "Service Requests | Dashboard",
        "sub_title": "Service Requests",
        "name": "Service Request List",
        "instances": instances,
    }
    return render(request, "panel/service-requests.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def service_requests_add(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:service_requests"))
        else:
            message = generate_form_errors(form)
    else:
        form = ServiceRequestForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Service Request",
        "sub_title": "Service Requests",
        "name": "Add Service Request",
        "form": form,
        "message": message,
    }
    return render(request, "panel/service-requests-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def service_requests_edit(request, id):
    instance = ServiceRequest.objects.get(id=id)

    if request.method == "POST":
        form = ServiceRequestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:service_requests"))
        else:
            message = generate_form_errors(form)
    else:
        form = ServiceRequestForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Service Request",
        "sub_title": "Service Requests",
        "name": "Edit Service Request",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/service-requests-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def service_requests_delete(request, id):
    instance = ServiceRequest.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:service_requests"))


def request_service_detail_view(request, id):
    instance = get_object_or_404(ServiceRequest, id=id)

    context = {
        "title": "Manager Dashboard | Request Details",
        "sub_title": "Requests",
        "name": "Service Request Details",
        "instance": instance,
    }
    return render(request, "panel/request-service-detail.html", context=context)



@login_required(login_url="/app/login")
@allow_manager
def coupons(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Coupon.objects.all()

    context = {
        "title": "Coupons | Dashboard",
        "sub_title": "Coupons",
        "name": "Coupons List",
        "instances": instances,
    }
    return render(request, "panel/coupons.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def coupons_add(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:coupons"))
        else:
            message = generate_form_errors(form)
    else:
        form = CouponForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Coupon",
        "sub_title": "Coupons",
        "name": "Add Coupon",
        "form": form,
        "message": message,
    }
    return render(request, "panel/coupons-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def coupons_edit(request, id):
    instance = Coupon.objects.get(id=id)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:coupons"))
        else:
            message = generate_form_errors(form)
    else:
        form = CouponForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Coupon",
        "sub_title": "Coupons",
        "name": "Edit Coupon",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/coupons-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def coupons_delete(request, id):
    instance = Coupon.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:coupons"))



@login_required(login_url="/app/login")
@allow_manager
def addresses(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Address.objects.all()

    context = {
        "title": "Addresses | Dashboard",
        "sub_title": "Addresses",
        "name": "Addresses List",
        "instances": instances,
    }
    return render(request, "panel/addresses.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def addresses_add(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:addresses"))
        else:
            message = generate_form_errors(form)
    else:
        form = AddressForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Address",
        "sub_title": "Addresses",
        "name": "Add Address",
        "form": form,
        "message": message,
    }
    return render(request, "panel/addresses-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def addresses_edit(request, id):
    instance = Address.objects.get(id=id)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:addresses"))
        else:
            message = generate_form_errors(form)
    else:
        form = AddressForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Address",
        "sub_title": "Addresses",
        "name": "Edit Address",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/addresses-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def addresses_delete(request, id):
    instance = Address.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:addresses"))


@login_required(login_url="/app/login")
@allow_manager
def cart_totals(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = CartTotal.objects.all()

    context = {
        "title": "Cart Totals | Dashboard",
        "sub_title": "Cart Totals",
        "name": "Cart Totals List",
        "instances": instances,
    }
    return render(request, "panel/cart-totals.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_totals_add(request):
    if request.method == "POST":
        form = CartTotalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:cart_totals"))
        else:
            message = generate_form_errors(form)
    else:
        form = CartTotalForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Cart Total",
        "sub_title": "Cart Totals",
        "name": "Add Cart Total",
        "form": form,
        "message": message,
    }
    return render(request, "panel/cart-totals-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_totals_edit(request, id):
    instance = CartTotal.objects.get(id=id)

    if request.method == "POST":
        form = CartTotalForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:cart_totals"))
        else:
            message = generate_form_errors(form)
    else:
        form = CartTotalForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Cart Total",
        "sub_title": "Cart Totals",
        "name": "Edit Cart Total",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/cart-totals-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_totals_delete(request, id):
    instance = CartTotal.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:cart_totals"))


@login_required(login_url="/app/login")
@allow_manager
def order_items(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = OrderItem.objects.all()

    context = {
        "title": "Order Items | Dashboard",
        "sub_title": "Order Items",
        "name": "Order Items List",
        "instances": instances,
    }
    return render(request, "panel/order-items.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def order_items_add(request):
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:order_items"))
        else:
            message = generate_form_errors(form)
    else:
        form = OrderItemForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Order Item",
        "sub_title": "Order Items",
        "name": "Add Order Item",
        "form": form,
        "message": message,
    }
    return render(request, "panel/order-items-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def order_items_edit(request, id):
    instance = OrderItem.objects.get(id=id)

    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:order_items"))
        else:
            message = generate_form_errors(form)
    else:
        form = OrderItemForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Order Item",
        "sub_title": "Order Items",
        "name": "Edit Order Item",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/order-items-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def order_items_delete(request, id):
    instance = OrderItem.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:order_items"))


@login_required(login_url="/app/login")
@allow_manager
def orders(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Order.objects.all()

    context = {
        "title": "Orders | Dashboard",
        "sub_title": "Orders",
        "name": "Orders List",
        "instances": instances,
    }
    return render(request, "panel/orders.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def orders_add(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:orders"))
        else:
            message = generate_form_errors(form)
    else:
        form = OrderForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Order",
        "sub_title": "Orders",
        "name": "Add Order",
        "form": form,
        "message": message,
    }
    return render(request, "panel/orders-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def orders_edit(request, id):
    instance = Order.objects.get(id=id)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:orders"))
        else:
            message = generate_form_errors(form)
    else:
        form = OrderForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Order",
        "sub_title": "Orders",
        "name": "Edit Order",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/orders-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def orders_delete(request, id):
    instance = Order.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:orders"))


@login_required(login_url="/app/login")
@allow_manager
def reviews(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Review.objects.all()

    context = {
        "title": "Reviews | Dashboard",
        "sub_title": "Reviews",
        "name": "Reviews List",
        "instances": instances,
    }
    return render(request, "panel/reviews.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def reviews_add(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:reviews"))
        else:
            message = generate_form_errors(form)
    else:
        form = ReviewForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Review",
        "sub_title": "Reviews",
        "name": "Add Review",
        "form": form,
        "message": message,
    }
    return render(request, "panel/reviews-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def reviews_edit(request, id):
    instance = Review.objects.get(id=id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:reviews"))
        else:
            message = generate_form_errors(form)
    else:
        form = ReviewForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Review",
        "sub_title": "Reviews",
        "name": "Edit Review",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/reviews-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def reviews_delete(request, id):
    instance = Review.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:reviews"))


@login_required(login_url="/app/login")
@allow_manager
def products(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Product.objects.all()

    context = {
        "title": "Products | Dashboard",
        "sub_title": "Products",
        "name": "Products List",
        "instances": instances,
    }
    return render(request, "panel/products.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def products_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:products"))
        else:
            message = generate_form_errors(form)
    else:
        form = ProductForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Product",
        "sub_title": "Products",
        "name": "Add Product",
        "form": form,
        "message": message,
    }
    return render(request, "panel/products-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def products_edit(request, id):
    instance = Product.objects.get(id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:products"))
        else:
            message = generate_form_errors(form)
    else:
        form = ProductForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Product",
        "sub_title": "Products",
        "name": "Edit Product",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/products-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def products_delete(request, id):
    instance = Product.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:products"))


@login_required(login_url="/app/login")
@allow_manager
def storages(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Storage.objects.all()

    context = {
        "title": "Storages | Dashboard",
        "sub_title": "Storages",
        "name": "Storages List",
        "instances": instances,
    }
    return render(request, "panel/storages.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def storages_add(request):
    if request.method == "POST":
        form = StorageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:storages"))
        else:
            message = generate_form_errors(form)
    else:
        form = StorageForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Storage",
        "sub_title": "Storages",
        "name": "Add Storage",
        "form": form,
        "message": message,
    }
    return render(request, "panel/storages-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def storages_edit(request, id):
    instance = Storage.objects.get(id=id)

    if request.method == "POST":
        form = StorageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:storages"))
        else:
            message = generate_form_errors(form)
    else:
        form = StorageForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Storage",
        "sub_title": "Storages",
        "name": "Edit Storage",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/storages-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def storages_delete(request, id):
    instance = Storage.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:storages"))


@login_required(login_url="/app/login")
@allow_manager
def icon_images(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = IconImage.objects.all().order_by('-id')

    context = {
        "title": "Icon Images | Dashboard",
        "sub_title": "Icon Images",
        "name": "Icon Images List",
        "instances": instances,
    }
    return render(request, "panel/icon-images.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def icon_images_add(request):
    if request.method == "POST":
        form = IconImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:icon_images"))
        else:
            message = generate_form_errors(form)
    else:
        form = IconImageForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Icon Image",
        "sub_title": "Icon Images",
        "name": "Add Icon Image",
        "form": form,
        "message": message,
    }
    return render(request, "panel/icon-images-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def icon_images_edit(request, id):
    instance = IconImage.objects.get(id=id)

    if request.method == "POST":
        form = IconImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:icon_images"))
        else:
            message = generate_form_errors(form)
    else:
        form = IconImageForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Icon Image",
        "sub_title": "Icon Images",
        "name": "Edit Icon Image",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/icon-images-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def icon_images_delete(request, id):
    instance = IconImage.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:icon_images"))




@login_required(login_url="/app/login")
@allow_manager
def specs(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Spec.objects.all().order_by('-id')

    context = {
        "title": "Specs | Dashboard",
        "sub_title": "Specs",
        "name": "Specs List",
        "instances": instances,
    }
    return render(request, "panel/specs.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def specs_add(request):
    if request.method == "POST":
        form = SpecForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:specs"))
        else:
            message = generate_form_errors(form)
    else:
        form = SpecForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Spec",
        "sub_title": "Specs",
        "name": "Add Spec",
        "form": form,
        "message": message,
    }
    return render(request, "panel/specs-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def specs_edit(request, id):
    instance = Spec.objects.get(id=id)

    if request.method == "POST":
        form = SpecForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:specs"))
        else:
            message = generate_form_errors(form)
    else:
        form = SpecForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Spec",
        "sub_title": "Specs",
        "name": "Edit Spec",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/specs-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def specs_delete(request, id):
    instance = Spec.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:specs"))



@login_required(login_url="/app/login")
@allow_manager
def customers(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Customer.objects.all()

    context = {
        "title": "Customers | Dashboard",
        "sub_title": "Customers",
        "name": "Customers List",
        "instances": instances,
    }
    return render(request, "panel/customers.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def customers_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:customers"))
        else:
            message = generate_form_errors(form)
    else:
        form = CustomerForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Customer",
        "sub_title": "Customers",
        "name": "Add Customer",
        "form": form,
        "message": message,
    }
    return render(request, "panel/customers-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def customers_edit(request, id):
    instance = Customer.objects.get(id=id)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:customers"))
        else:
            message = generate_form_errors(form)
    else:
        form = CustomerForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Customer",
        "sub_title": "Customers",
        "name": "Edit Customer",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/customers-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def customers_delete(request, id):
    instance = Customer.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:customers"))

@login_required(login_url="/app/login")
@allow_manager
def cart_items(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = CartItem.objects.all()

    context = {
        "title": "Cart Items | Dashboard",
        "sub_title": "Cart Items",
        "name": "Cart Items List",
        "instances": instances,
    }
    return render(request, "panel/cart-items.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_items_add(request):
    if request.method == "POST":
        form = CartItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:cart_items"))
        else:
            message = generate_form_errors(form)
    else:
        form = CartItemForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Cart Item",
        "sub_title": "Cart Items",
        "name": "Add Cart Item",
        "form": form,
        "message": message,
    }
    return render(request, "panel/cart-items-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_items_edit(request, id):
    instance = CartItem.objects.get(id=id)

    if request.method == "POST":
        form = CartItemForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:cart_items"))
        else:
            message = generate_form_errors(form)
    else:
        form = CartItemForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Cart Item",
        "sub_title": "Cart Items",
        "name": "Edit Cart Item",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/cart-items-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_items_delete(request, id):
    instance = CartItem.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:cart_items"))


@login_required(login_url="/app/login")
@allow_manager
def whishlist(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Whishlist.objects.all()

    context = {
        "title": "Whishlist | Dashboard",
        "sub_title": "Whishlist",
        "name": "Whishlist Items",
        "instances": instances,
    }
    return render(request, "panel/whishlist.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def whishlist_add(request):
    if request.method == "POST":
        form = WhishlistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:whishlist"))
        else:
            message = generate_form_errors(form)
    else:
        form = WhishlistForm()
        message = None

    context = {
        "title": "Manager Dashboard | Add Whishlist Item",
        "sub_title": "Whishlist",
        "name": "Add Whishlist Item",
        "form": form,
        "message": message,
    }
    return render(request, "panel/whishlist-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def whishlist_edit(request, id):
    instance = Whishlist.objects.get(id=id)

    if request.method == "POST":
        form = WhishlistForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:whishlist"))
        else:
            message = generate_form_errors(form)
    else:
        form = WhishlistForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Whishlist Item",
        "sub_title": "Whishlist",
        "name": "Edit Whishlist Item",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/whishlist-add.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def whishlist_delete(request, id):
    instance = Whishlist.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:whishlist"))



@login_required(login_url="/app/login")
@allow_manager
def user_list(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = User.objects.all()
    context = {
        "title": "Users | Dashboard",
        "sub_title": "Users",
        "name": "User List",
        "instances": instances,
    }
    return render(request, "panel/users.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def user_add(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:user_list"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add User",
                "sub_title": "Users",
                "name": "Add User",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/add-user.html", context=context)

    form = UserForm()
    context = {
        "title": "Manager Dashboard | Add User",
        "sub_title": "Users",
        "name": "Add User",
        "form": form,
    }
    return render(request, "panel/add-user.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def user_edit(request, pk):
    instance = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:user_list"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit User",
                "sub_title": "Users",
                "name": "Edit User",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/add-user.html", context=context)

    form = UserForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit User",
        "sub_title": "Users",
        "name": "Edit User",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/add-user.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def user_delete(request, pk):
    instance = get_object_or_404(User, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:user_list"))




@login_required(login_url="/app/login")
@allow_manager
def otpverifier_list(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = OTPVerifier.objects.all()
    context = {
        "title": "OTP Verifiers | Dashboard",
        "sub_title": "OTP Verifiers",
        "name": "OTP Verifier List",
        "instances": instances,
    }
    return render(request, "panel/otp-verifiers.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def sliders(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Slider.objects.all()
    context = {
        "title": "Sliders | Dashboard",
        "sub_title": "Sliders",
        "name": "Slider List",
        "instances": instances,
    }
    return render(request, "panel/sliders.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def slider_add(request):
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:sliders"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Slider",
                "sub_title": "Sliders",
                "name": "Add Slider",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/add-slider.html", context=context)

    form = SliderForm()
    context = {
        "title": "Manager Dashboard | Add Slider",
        "sub_title": "Sliders",
        "name": "Add Slider",
        "form": form,
    }
    return render(request, "panel/add-slider.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def slider_edit(request, pk):
    instance = get_object_or_404(Slider, pk=pk)
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:sliders"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Slider",
                "sub_title": "Sliders",
                "name": "Edit Slider",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/add-slider.html", context=context)

    form = SliderForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Slider",
        "sub_title": "Sliders",
        "name": "Edit Slider",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/add-slider.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def slider_delete(request, pk):
    instance = get_object_or_404(Slider, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:sliders"))


@login_required(login_url="/app/login")
@allow_manager
def offer_list(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Offer.objects.all()
    context = {
        "title": "Offers | Dashboard",
        "sub_title": "Offers",
        "name": "Offer List",
        "instances": instances,
    }
    return render(request, "panel/offers.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offer_add(request):
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:offer"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Offer",
                "sub_title": "Offers",
                "name": "Add Offer",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/add-offer.html", context=context)

    form = OfferForm()
    context = {
        "title": "Manager Dashboard | Add Offer",
        "sub_title": "Offers",
        "name": "Add Offer",
        "form": form,
    }
    return render(request, "panel/add-offer.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offer_edit(request, pk):
    instance = get_object_or_404(Offer, pk=pk)
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:offer"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Offer",
                "sub_title": "Offers",
                "name": "Edit Offer",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/add-offer.html", context=context)

    form = OfferForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Offer",
        "sub_title": "Offers",
        "name": "Edit Offer",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/add-offer.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offer_delete(request, pk):
    instance = get_object_or_404(Offer, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:offer"))


@login_required(login_url="/app/login")
@allow_manager
def offers_list(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    instances = Offers.objects.all()
    context = {
        "title": "Offers List | Dashboard",
        "sub_title": "Offers List",
        "name": "Offers List",
        "instances": instances,
    }
    return render(request, "panel/offers-list.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offers_add(request):
    if request.method == "POST":
        form = OffersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:offers"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Add Offers",
                "sub_title": "Offers",
                "name": "Add Offers",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "panel/add-offers.html", context=context)

    form = OffersForm()
    context = {
        "title": "Manager Dashboard | Add Offers",
        "sub_title": "Offers",
        "name": "Add Offers",
        "form": form,
    }
    return render(request, "panel/add-offers.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offers_edit(request, pk):
    instance = get_object_or_404(Offers, pk=pk)
    if request.method == "POST":
        form = OffersForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:offers"))
        else:
            message = generate_form_errors(form)
            context = {
                "title": "Manager Dashboard | Edit Offers",
                "sub_title": "Offers",
                "name": "Edit Offers",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "panel/add-offers.html", context=context)

    form = OffersForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Offers",
        "sub_title": "Offers",
        "name": "Edit Offers",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/add-offers.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def offers_delete(request, pk):
    instance = get_object_or_404(Offers, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:offers"))
