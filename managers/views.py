from django.shortcuts import render
import datetime
from django.db.models import Sum

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_manager
from main.functions import generate_form_errors

from promos.models import *
from items.models import *
from users.models import *
from customers.models import *
from managers.forms import *

@login_required(login_url="/app/login")
@allow_manager
def categories(request):
    instances = Category.objects.all()
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
            return render(request, "panel/categories-edit.html", context=context)

    form = CategoryForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Category",
        "sub_title": "Categories",
        "name": "Edit Category",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/categories-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def categories_delete(request, id):
    instance = Category.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:categories"))


@login_required(login_url="/app/login")
@allow_manager
def brands(request):
    instances = Brand.objects.all()
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
            return render(request, "panel/brands-edit.html", context=context)

    form = BrandForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Brand",
        "sub_title": "Brands",
        "name": "Edit Brand",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/brands-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def brands_delete(request, id):
    instance = Brand.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:brands"))


@login_required(login_url="/app/login")
@allow_manager
def colors(request):
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
            return render(request, "panel/colors-edit.html", context=context)

    form = ColorForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Color",
        "sub_title": "Colors",
        "name": "Edit Color",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/colors-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def colors_delete(request, id):
    instance = Color.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:colors"))


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications(request):
    instances = CustomSpecification.objects.all()
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
            return render(request, "panel/custom-specifications-edit.html", context=context)

    form = CustomSpecificationForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Custom Specification",
        "sub_title": "Custom Specifications",
        "name": "Edit Custom Specification",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/custom-specifications-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def custom_specifications_delete(request, id):
    instance = CustomSpecification.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:custom_specifications"))


@login_required(login_url="/app/login")
@allow_manager
def options(request):
    instances = Option.objects.all()
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
            return render(request, "panel/options-edit.html", context=context)

    form = OptionForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Option",
        "sub_title": "Options",
        "name": "Edit Option",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/options-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def options_delete(request, id):
    instance = Option.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:options"))



@login_required(login_url="/app/login")
@allow_manager
def product_images(request):
    instances = ProductImage.objects.all()
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
            return render(request, "panel/product-images-edit.html", context=context)

    form = ProductImageForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit Product Image",
        "sub_title": "Product Images",
        "name": "Edit Product Image",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/product-images-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def product_images_delete(request, id):
    instance = ProductImage.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:product_images"))



@login_required(login_url="/app/login")
@allow_manager
def rams(request):
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
            return render(request, "panel/rams-edit.html", context=context)

    form = RamForm(instance=instance)
    context = {
        "title": "Manager Dashboard | Edit RAM",
        "sub_title": "RAMs",
        "name": "Edit RAM",
        "form": form,
        "instance": instance,
    }
    return render(request, "panel/rams-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def rams_delete(request, id):
    instance = Ram.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:rams"))


@login_required(login_url="/app/login")
@allow_manager
def services(request):
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
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:services"))
        else:
            message = generate_form_errors(form)
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
    instance = Service.objects.get(id=id)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:services"))
        else:
            message = generate_form_errors(form)
    else:
        form = ServiceForm(instance=instance)
        message = None

    context = {
        "title": "Manager Dashboard | Edit Service",
        "sub_title": "Services",
        "name": "Edit Service",
        "form": form,
        "message": message,
        "instance": instance,
    }
    return render(request, "panel/services-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def services_delete(request, id):
    instance = Service.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:services"))



@login_required(login_url="/app/login")
@allow_manager
def service_requests(request):
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
    return render(request, "panel/service-requests-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def service_requests_delete(request, id):
    instance = ServiceRequest.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:service_requests"))



@login_required(login_url="/app/login")
@allow_manager
def coupons(request):
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
    return render(request, "panel/coupons-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def coupons_delete(request, id):
    instance = Coupon.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:coupons"))



@login_required(login_url="/app/login")
@allow_manager
def addresses(request):
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
    return render(request, "panel/addresses-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def addresses_delete(request, id):
    instance = Address.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:addresses"))


@login_required(login_url="/app/login")
@allow_manager
def cart_totals(request):
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
    return render(request, "panel/cart-totals-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def cart_totals_delete(request, id):
    instance = CartTotal.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:cart_totals"))


@login_required(login_url="/app/login")
@allow_manager
def order_items(request):
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
    return render(request, "panel/order-items-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def order_items_delete(request, id):
    instance = OrderItem.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:order_items"))


@login_required(login_url="/app/login")
@allow_manager
def orders(request):
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
    return render(request, "panel/orders-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def orders_delete(request, id):
    instance = Order.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:orders"))


@login_required(login_url="/app/login")
@allow_manager
def reviews(request):
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
    return render(request, "panel/reviews-edit.html", context=context)


@login_required(login_url="/app/login")
@allow_manager
def reviews_delete(request, id):
    instance = Review.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("managers:reviews"))

