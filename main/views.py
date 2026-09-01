from urllib import request
from decimal import Decimal
from datetime import datetime

from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User

from functools import wraps

import uuid


from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from django.utils.html import strip_tags

from django.conf import settings

from .forms import CustomerRegisterForm

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.http import HttpResponse


from .models import (
    HeroSection, Category, Destination, MiddleBanner, Deal,
    CallSection, FooterQuickLink, FooterCategory, FooterContact, Payment,
    SocialLink, Tour, UserAdminProfile, Vendor, Blog, BlogCategory, Wishlist, WishlistBanner, CustomerWishlist, DriverApplication, Destination, SEOSettings, Hotel, HotelImage, TourImage, Booking, HotelBooking,

)

from main.forms import VendorRegisterForm, UserAdminRegisterForm, HotelForm, TourForm
from django.contrib.auth import get_user_model

User = get_user_model()



# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------
def home(request):
    hero = HeroSection.objects.first()
    categories = Category.objects.all()
    destinations = Destination.objects.all()
    middle_banner = MiddleBanner.objects.first()
    deals = Deal.objects.all()
    call_section = CallSection.objects.first()

    footer_quick_links = FooterQuickLink.objects.all()
    footer_categories = FooterCategory.objects.all()
    footer_contact = FooterContact.objects.first()
    social_links = SocialLink.objects.all()

    vendors = Vendor.objects.filter(verified=True).order_by("-rating")[:6]

        # ✅ SEO from Admin
    seo = SEOSettings.objects.filter(page_name="home").first()

    tours = (
        Tour.objects.filter(status="Active")
            .select_related("profile")
            .prefetch_related("images")
            .order_by("-id")[:6]
        )
    hotels = Hotel.objects.order_by("-id")[:6]

    is_customer = False

    if request.user.is_authenticated:
        is_customer = not UserAdminProfile.objects.filter(
            user=request.user
        ).exists()

    context = {
        "hero": hero,
        "categories": categories,
        "destinations": destinations,
        "middle_banner": middle_banner,
        "deals": deals,
        "call_section": call_section,

        "footer_quick_links": footer_quick_links,
        "footer_categories": footer_categories,
        "footer_contact": footer_contact,
        "social_links": social_links,
        "vendors": vendors,
        "tours": tours,
        "hotels": hotels,

        "is_customer": is_customer,

                # 🔥 SEO CONTEXT
        "seo": seo,
    }
    return render(request, "index.html", context)


def admin_only(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("user_admin_login")

        if not hasattr(request.user, "admin_profile"):
            logout(request)
            return redirect("user_admin_login")

        return view_func(request, *args, **kwargs)

    return wrapper


def category_tours(request, category_id):
    # ૧. જે કેટેગરી પર ક્લિક કર્યું તેની વિગત મેળવો
    category = get_object_or_404(Category, id=category_id)
    
    # ૨. તે કેટેગરીની બધી જ એક્ટિવ ટૂર્સ ફિલ્ટર કરો
    # (નોંધ: તમારા Tour મોડેલમાં category ની ForeignKey નું જે નામ હોય તે અહીં લખવું)
    tours = Tour.objects.filter(category=category, status="Active")
    
    context = {
        'category': category,
        'tours': tours,
    }
    return render(request, 'category_tours.html', context)    


def customer_only(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User is not logged in
        if not request.user.is_authenticated:
            return redirect("customer_login")

        # Owner / Admin cannot access Customer pages
        if hasattr(request.user, "admin_profile"):
            logout(request)
            return redirect("customer_login")

        # Vendor cannot access Customer pages
        if getattr(request.user, "role", None) == "vendor":
            logout(request)
            return redirect("customer_login")

        # Customer is allowed
        return view_func(request, *args, **kwargs)

    return wrapper



def vendor_only(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Not logged in
        if not request.user.is_authenticated:
            return redirect("vendor_login")

        # Owner/Admin cannot access Vendor Dashboard
        if hasattr(request.user, "admin_profile"):
            logout(request)
            return redirect("vendor_login")

        # Only Vendor allowed
        if getattr(request.user, "role", None) != "vendor":
            logout(request)
            return redirect("vendor_login")

        return view_func(request, *args, **kwargs)

    return wrapper

# ----------------------------------------------------
# VENDOR REGISTRATION (NO LOGIN REQUIRED)
# ----------------------------------------------------
def vendor_register(request):

    if request.method == "POST":
        form = VendorRegisterForm(request.POST, request.FILES)

        if form.is_valid():

            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone")

            # 1) USER ACCOUNT CREATE
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already registered! Please login.")
                return redirect("vendor_login")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            user.role = "vendor"
            user.phone = phone

            user.save()

            # 2) CREATE VENDOR PROFILE
            vendor = form.save(commit=False)
            vendor.user = user
            vendor.save()

            # 3) AUTO LOGIN AFTER REGISTER
            login(request, user)

            return redirect("vendor_success")

    else:
        form = VendorRegisterForm()

    return render(request, "vendor/vendor_register.html", {"form": form})



# ----------------------------------------------------
# VENDOR LOGIN (FINAL — only ONE definition)
# ----------------------------------------------------
def vendor_login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user:
            if user.role == "vendor":
                login(request, user)
                return redirect("vendor_dashboard")
            else:
                messages.error(request, "This is not a vendor account.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "vendor/vendor_login.html")



# ----------------------------------------------------
# VENDOR DASHBOARD
# ----------------------------------------------------
@vendor_only
def vendor_dashboard(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    return render(request, "vendor/vendor_dashboard.html", {"vendor": vendor})



# ----------------------------------------------------
# VENDOR SUCCESS PAGE
# ----------------------------------------------------
def vendor_success(request):
    return render(request, "vendor/vendor_success.html")


# ----------------------------------------------------
# BLOG LIST PAGE (DYNAMIC)
# ----------------------------------------------------
def blog_list(request):
    search = request.GET.get("q")
    category_slug = request.GET.get("category")

    blogs = Blog.objects.all().order_by("-created_at")

    # SEARCH
    if search:
        blogs = blogs.filter(title__icontains=search)

    # CATEGORY FILTER
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)

    # PAGINATION
    paginator = Paginator(blogs, 6)
    page = request.GET.get("page")
    blogs = paginator.get_page(page)

    categories = BlogCategory.objects.all()
    latest_posts = Blog.objects.order_by("-created_at")[:3]

    context = {
        "blogs": blogs,
        "categories": categories,
        "latest_posts": latest_posts,
    }
    return render(request, "blog.html", context)



# ----------------------------------------------------
# BLOG DETAIL PAGE
# ----------------------------------------------------
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # latest posts sidebar
    latest_posts = Blog.objects.exclude(id=blog.id).order_by("-created_at")[:3]

    context = {
        "blog": blog,
        "latest_posts": latest_posts
    }
    return render(request, "blog_detail.html", context)


def contact_page(request):
    return render(request, 'contact.html')


def wishlist_page(request):
    wishlist = Wishlist.objects.all()
    banner = WishlistBanner.objects.first()
    return render(request, "wishlist.html", {
        "wishlist": wishlist,
        "banner": banner,
    })




def become_driver(request):
    if request.method == "POST":

        availability = request.POST.getlist("availability")
        availability_str = ", ".join(availability)

        DriverApplication.objects.create(
            city=request.POST.get("city"),
            service_area=request.POST.get("service_area"),

            vehicle_type=request.POST.get("vehicle_type"),
            vehicle_model=request.POST.get("vehicle_model"),
            vehicle_number=request.POST.get("vehicle_number"),

            experience_years=request.POST.get("experience_years") or 0,
            airport_experience=request.POST.get("airport_experience"),

            availability=availability_str,

            driving_license=request.FILES.get("driving_license"),
            vehicle_rc=request.FILES.get("vehicle_rc"),
            id_proof=request.FILES.get("id_proof"),
            vehicle_photo=request.FILES.get("vehicle_photo"),

            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            bank_account=request.POST.get("bank_account"),
        )

        messages.success(request, "Application submitted successfully!")
        return redirect("home")

    return render(request, "become_driver.html")


# ----------------------------------------------------
# MY ACCOUNT PAGE
# ----------------------------------------------------
@login_required
def my_account(request):
    footer_quick_links = FooterQuickLink.objects.all()
    footer_categories = FooterCategory.objects.all()
    footer_contact = FooterContact.objects.first()
    social_links = SocialLink.objects.all()

    context = {
        "user": request.user,
        "footer_quick_links": footer_quick_links,
        "footer_categories": footer_categories,
        "footer_contact": footer_contact,
        "social_links": social_links,
    }
    return render(request, "account.html", context)


# ----------------------------------------------------
# HELP PAGE
# ----------------------------------------------------
def help_page(request):
    footer_quick_links = FooterQuickLink.objects.all()
    footer_categories = FooterCategory.objects.all()
    footer_contact = FooterContact.objects.first()
    social_links = SocialLink.objects.all()

    context = {
        "footer_quick_links": footer_quick_links,
        "footer_categories": footer_categories,
        "footer_contact": footer_contact,
        "social_links": social_links,
    }
    return render(request, "help.html", context)


def search_results(request):
    query = request.GET.get("q")
    date = request.GET.get("date")

    destinations = Destination.objects.all()

    if query:
        destinations = destinations.filter(
            Q(title__icontains=query) |
            Q(country_category__icontains=query)
        )

    context = {
        "query": query,
        "date": date,
        "destinations": destinations
    }

    return render(request, "search_results.html", context)


def user_admin_login(request):

    if request.user.is_authenticated:

        if hasattr(request.user, "admin_profile"):
            return redirect("user_dashboard")

        logout(request)

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if user:

            # માત્ર Admin Panel User જ Login કરી શકે
            if not hasattr(user, "admin_profile"):

                messages.error(
                    request,
                    "This account is not registered as an Admin Panel user."
                )

                return redirect("user_admin_login")

            login(request, user)
            return redirect("user_dashboard")

        messages.error(
            request,
            "Invalid Email or Password."
        )

    return render(
        request,
        "user_admin/login.html"
    )



def user_admin_register(request):

    if request.method == "POST":

        form = UserAdminRegisterForm(request.POST, request.FILES)

        if form.is_valid():

            print("✅ FORM VALID")

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=email).exists():
                print("❌ EMAIL EXISTS")
                messages.error(request, "Email already exists.")
                return redirect("user_admin_register")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)

            print("✅ USER CREATED")

            return redirect("user_dashboard")

        else:
            print("❌ FORM INVALID")
            print(form.errors)

    else:
        form = UserAdminRegisterForm()

    return render(
        request,
        "user_admin/register.html",
        {
            "form": form
        }
    )




@admin_only
def user_dashboard(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:

        messages.error(
            request,
            "Please create your Admin Panel first."
        )

        return redirect("user_admin_register")

    total_hotels = Hotel.objects.filter(
        profile=profile
    ).count()

    total_tours = Tour.objects.filter(
        profile=profile
    ).count()

    return render(
        request,
        "user_admin/dashboard.html",
        {
            "profile": profile,
            "total_hotels": total_hotels,
            "total_tours": total_tours,
        }
    )


def user_logout(request):
    logout(request)
    return redirect("home")    


@admin_only
def hotel_list(request):

    profile = UserAdminProfile.objects.get(
        user=request.user
    )

    hotels = Hotel.objects.filter(
        profile=profile
    )

    return render(
        request,
        "user_admin/hotels/hotel_list.html",
        {
            "hotels": hotels
        }
    )


@admin_only
def hotel_add(request):

    profile = UserAdminProfile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        form = HotelForm(request.POST)

        if form.is_valid():

            hotel = form.save(commit=False)

            hotel.profile = profile

            hotel.save()

            messages.success(
                request,
                "Hotel Added Successfully."
            )

            return redirect("hotel_list")

    else:

        form = HotelForm()

    return render(
        request,
        "user_admin/hotels/hotel_add.html",
        {
            "form": form
        }
    )

@admin_only
def hotel_images(request):

    profile = UserAdminProfile.objects.get(user=request.user)

    hotels = Hotel.objects.filter(profile=profile)

    if request.method == "POST":

        hotel = request.POST.get("hotel")
        images = request.FILES.getlist("image")   # <-- બદલ્યું

        if hotel and images:

            for image in images:

                HotelImage.objects.create(
                    hotel_id=hotel,
                    image=image
                )

            messages.success(
                request,
                "Images Uploaded Successfully."
            )

            return redirect("hotel_images")

    images = HotelImage.objects.filter(
        hotel__profile=profile
    )

    return render(
        request,
        "user_admin/hotels/hotel_images.html",
        {
            "hotels": hotels,
            "images": images,
        }
    )


@admin_only
def hotel_view(request, id):

    profile = UserAdminProfile.objects.get(user=request.user)

    hotel = get_object_or_404(
        Hotel,
        id=id,
        profile=profile
    )

    return render(
        request,
        "user_admin/hotels/hotel_view.html",
        {
            "hotel": hotel
        }
    )


@admin_only
def hotel_edit(request, id):

    profile = UserAdminProfile.objects.get(user=request.user)

    hotel = get_object_or_404(
        Hotel,
        id=id,
        profile=profile
    )

    if request.method == "POST":

        form = HotelForm(request.POST, instance=hotel)

        if form.is_valid():

            form.save()

            messages.success(request, "Hotel Updated Successfully.")

            return redirect("hotel_list")

    else:

        form = HotelForm(instance=hotel)

    return render(
        request,
        "user_admin/hotels/hotel_add.html",
        {
            "form": form
        }
    )


@admin_only
def hotel_delete(request, id):

    profile = UserAdminProfile.objects.get(user=request.user)

    hotel = get_object_or_404(
        Hotel,
        id=id,
        profile=profile
    )

    hotel.delete()

    messages.success(
        request,
        "Hotel Deleted Successfully."
    )

    return redirect("hotel_list")


@admin_only
def hotel_image_delete(request, id):

    profile = UserAdminProfile.objects.get(user=request.user)

    image = get_object_or_404(
        HotelImage,
        id=id,
        hotel__profile=profile
    )

    # ફાઇલ પણ delete થશે
    if image.image:
        image.image.delete(save=False)

    image.delete()

    messages.success(
        request,
        "Image Deleted Successfully."
    )

    return redirect("hotel_images")


@admin_only
def tour_list(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    tours = Tour.objects.filter(
        profile=profile
    ).prefetch_related(
        "images"
    ).order_by("-id")

    context = {
        "tours": tours
    }

    return render(
        request,
        "user_admin/tours/tour_list.html",
        context
    )


@admin_only
def tour_add(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        form = TourForm(request.POST)

        files = request.FILES.getlist("images")

        if form.is_valid():

            tour = form.save(commit=False)

            tour.profile = profile

            tour.save()

            for file in files:

                TourImage.objects.create(
                    tour=tour,
                    image=file
                )

            messages.success(
                request,
                "Tour Added Successfully."
            )

            return redirect("tour_list")

    else:

        form = TourForm()

    context = {

        "form": form

    }

    return render(
        request,
        "user_admin/tours/tour_add.html",
        context
    )

@admin_only
def tour_view(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    tour = get_object_or_404(
        Tour.objects.prefetch_related("images"),
        id=pk,
        profile=profile
    )

    context = {

        "tour": tour,

        "images": tour.images.all()

    }

    return render(
        request,
        "user_admin/tours/tour_view.html",
        context
    )


@admin_only
def tour_edit(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    tour = get_object_or_404(
        Tour,
        id=pk,
        profile=profile
    )

    if request.method == "POST":

        form = TourForm(
            request.POST,
            instance=tour
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Tour Updated Successfully."
            )

            return redirect("tour_list")

    else:

        form = TourForm(
            instance=tour
        )

    context = {

        "form": form,
        "tour": tour

    }

    return render(
        request,
        "user_admin/tours/tour_edit.html",
        context
    )


@admin_only
def tour_delete(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    tour = get_object_or_404(
        Tour,
        id=pk,
        profile=profile
    )

    tour.delete()

    messages.success(
        request,
        "Tour Deleted Successfully."
    )

    return redirect("tour_list")


@admin_only
def tour_images(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    tours = Tour.objects.filter(
        profile=profile
    )

    images = TourImage.objects.filter(
        tour__profile=profile
    ).order_by("-id")

    if request.method == "POST":

        tour = request.POST.get("tour")

        files = request.FILES.getlist("image")

        selected_tour = get_object_or_404(
            Tour,
            id=tour,
            profile=profile
        )

        for file in files:

            TourImage.objects.create(
                tour=selected_tour,
                image=file
            )

        messages.success(
            request,
            "Images Uploaded Successfully."
        )

        return redirect("tour_images")

    context = {

        "tours": tours,
        "images": images

    }

    return render(
        request,
        "user_admin/tours/tour_images.html",
        context
    )    


@admin_only
def tour_image_delete(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    image = get_object_or_404(
        TourImage,
        id=pk,
        tour__profile=profile
    )

    image.delete()

    messages.success(
        request,
        "Tour Image Deleted Successfully."
    )

    return redirect("tour_images")


@admin_only
def booking_list(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        profile=profile
    ).select_related("tour").order_by("-id")

    context = {
        "bookings": bookings
    }

    return render(
        request,
        "user_admin/bookings/booking_list.html",
        context
    )


@admin_only
def booking_view(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        Booking,
        id=pk,
        profile=profile
    )

    return render(
        request,
        "user_admin/bookings/booking_view.html",
        {
            "booking": booking
        }
    )


@admin_only
def booking_pending(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        profile=profile,
        status="Pending"
    )

    return render(
        request,
        "user_admin/bookings/booking_pending.html",
        {
            "bookings": bookings
        }
    )


@admin_only
def booking_confirm(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        Booking,
        id=pk,
        profile=profile
    )

    booking.status = "Confirmed"
    booking.save()

    return redirect("booking_list")


@admin_only
def booking_cancel(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        Booking,
        id=pk,
        profile=profile
    )

    booking.status = "Cancelled"
    booking.save()

    return redirect("booking_list")


@admin_only
def booking_confirmed(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        profile=profile,
        status="Confirmed"
    )

    return render(
        request,
        "user_admin/bookings/booking_confirmed.html",
        {
            "bookings": bookings
        }
    )

@admin_only
def booking_cancelled(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        profile=profile,
        status="Cancelled"
    )

    return render(
        request,
        "user_admin/bookings/booking_cancelled.html",
        {
            "bookings": bookings
        }
    )


def tour_detail(request, pk):

    tour = get_object_or_404(
        Tour.objects.prefetch_related("images"),
        id=pk,
        status="Active"
    )

    return render(
        request,
        "tours/detail.html",
        {
            "tour": tour,
            "images": tour.images.all()
        }
    )



@customer_only
def tour_booking(request, pk):

    tour = get_object_or_404(
        Tour,
        id=pk,
        status="Active"
    )

    if request.method == "POST":

        persons = int(
            request.POST.get("persons")
        )

        total_amount = (
            Decimal(tour.price) * persons
        )

        booking = Booking.objects.create(

            profile=tour.profile,

            tour=tour,

            # Logged-in Customer
            customer_name=(
                request.user.get_full_name()
                or request.user.username
            ),

            customer_email=request.user.email,

            customer_phone=request.POST.get(
                "customer_phone"
            ),

            persons=persons,

            booking_date=request.POST.get(
                "booking_date"
            ),

            total_amount=total_amount,
        )

        html_content = render_to_string(
            "emails/booking_confirmation.html",
            {
                "booking": booking,
            }
        )

        text_content = strip_tags(
            html_content
        )

        email = EmailMultiAlternatives(
            subject="TravelBiz Booking Confirmation",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.customer_email],
        )

        email.attach_alternative(
            html_content,
            "text/html"
        )

        email.send()

        messages.success(
            request,
            "Your tour booking has been submitted successfully."
        )

        return redirect(
            "tour_detail",
            pk=tour.id
        )

    return render(
        request,
        "tours/booking.html",
        {
            "tour": tour
        }
    )



@login_required
def booking_invoice(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        Booking,
        id=pk,
        profile=profile
    )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="Booking_{booking.id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>TravelBiz</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Booking Invoice", styles["Heading2"])
    )

    data = [

        ["Booking ID", str(booking.id)],

        ["Customer", booking.customer_name],

        ["Email", booking.customer_email],

        ["Phone", booking.customer_phone],

        ["Tour", booking.tour.tour_name],

        ["Location", booking.tour.location],

        ["Travel Date", str(booking.booking_date)],

        ["Persons", str(booking.persons)],

        ["Amount", f"₹ {booking.total_amount}"],

        ["Status", booking.status],

    ]

    table = Table(data, colWidths=[2.2 * inch, 3.5 * inch])

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.green),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

    ]))

    elements.append(table)

    doc.build(elements)

    return response


@admin_only
def hotel_booking_invoice(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        profile=profile
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Hotel_Booking_{booking.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    elements = []

    # =========================
    # HEADER
    # =========================

    elements.append(
        Paragraph(
            "<b>TravelBiz</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Hotel Booking Invoice",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # PAYMENT INFORMATION
    # =========================

    payment = getattr(
        booking,
        "payment",
        None
    )

    transaction_id = "-"

    if payment and payment.transaction_id:
        transaction_id = payment.transaction_id

    # =========================
    # BOOKING INFORMATION
    # =========================

    data = [
        ["Booking ID", f"#{booking.id}"],

        [
            "Customer",
            booking.customer_name or "-"
        ],

        [
            "Email",
            booking.customer_email or "-"
        ],

        [
            "Phone",
            booking.customer_phone or "-"
        ],

        [
            "Hotel",
            booking.hotel.hotel_name
        ],

        [
            "Location",
            booking.hotel.location
        ],

        [
            "Check In",
            str(booking.check_in)
        ],

        [
            "Check Out",
            str(booking.check_out)
        ],

        [
            "Rooms",
            str(booking.rooms)
        ],

        [
            "Guests",
            str(booking.guests)
        ],

        [
            "Amount",
            f"₹ {booking.total_amount}"
        ],

        [
            "Booking Status",
            booking.status
        ],

        [
            "Payment Status",
            booking.payment_status
        ],

        [
            "Transaction ID",
            transaction_id
        ],
    ]

    table = Table(
        data,
        colWidths=[
            2.2 * inch,
            3.5 * inch
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.green
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 1),
                (0, -1),
                colors.whitesmoke
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                10
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),
        ])
    )

    elements.append(table)

    doc.build(elements)

    return response        


def hotel_detail(request, pk):

    hotel = get_object_or_404(
        Hotel.objects.prefetch_related("images"),
        id=pk,
        status=True
    )

    return render(
        request,
        "hotels/detail.html",
        {
            "hotel": hotel,
            "images": hotel.images.all(),
        }
    )  


@customer_only
def hotel_booking(request, pk):

    hotel = get_object_or_404(
        Hotel,
        id=pk,
        status=True
    )

    if request.method == "POST":

        rooms = int(request.POST.get("rooms"))
        guests = int(request.POST.get("guests"))

        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        # Calculate number of nights
        check_in_date = datetime.strptime(
            check_in,
            "%Y-%m-%d"
        ).date()

        check_out_date = datetime.strptime(
            check_out,
            "%Y-%m-%d"
        ).date()

        days = (check_out_date - check_in_date).days

        # Check valid dates
        if days <= 0:
            messages.error(
                request,
                "Check-out date must be after check-in date."
            )

            return redirect(
                "hotel_booking",
                pk=hotel.id
            )

        # Calculate total
        total_amount = (
            Decimal(hotel.price) * rooms * days
        )

        booking = HotelBooking.objects.create(

            profile=hotel.profile,

            hotel=hotel,

            customer_name=(
                request.user.get_full_name()
                or request.user.username
            ),

            customer_email=request.user.email,

            customer_phone=request.POST.get(
                "customer_phone"
            ),

            check_in=check_in_date,

            check_out=check_out_date,

            rooms=rooms,

            guests=guests,

            total_amount=total_amount,
        )

        messages.success(
            request,
            "Hotel booking submitted successfully."
        )

        return redirect(
            "hotel_detail",
            pk=hotel.id
        )

    return render(
        request,
        "hotels/booking.html",
        {
            "hotel": hotel
        }
    )


@admin_only
def hotel_booking_list(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = HotelBooking.objects.filter(
        profile=profile
    ).select_related("hotel").order_by("-id")

    return render(
        request,
        "user_admin/hotel_bookings/hotel_booking_list.html",
        {
            "bookings": bookings
        }
    )


@admin_only
def hotel_booking_view(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        profile=profile
    )

    return render(
        request,
        "user_admin/hotel_bookings/hotel_booking_view.html",
        {
            "booking": booking
        }
    )


@admin_only
def hotel_booking_confirm(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        profile=profile
    )

    booking.status = "Confirmed"
    booking.save()

    messages.success(
        request,
        "Booking Confirmed Successfully."
    )

    return redirect("hotel_booking_list")


@admin_only
def hotel_booking_cancel(request, pk):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        profile=profile
    )

    booking.status = "Cancelled"
    booking.save()

    messages.success(
        request,
        "Booking Cancelled Successfully."
    )

    return redirect("hotel_booking_list")


@admin_only
def hotel_booking_confirmed(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = HotelBooking.objects.filter(
        profile=profile,
        status="Confirmed"
    )

    return render(
        request,
        "user_admin/hotel_bookings/hotel_booking_confirmed.html",
        {
            "bookings": bookings
        }
    )


@admin_only
def hotel_booking_cancelled(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = HotelBooking.objects.filter(
        profile=profile,
        status="Cancelled"
    )

    return render(
        request,
        "user_admin/hotel_bookings/hotel_booking_cancelled.html",
        {
            "bookings": bookings
        }
    )


@admin_only
def hotel_booking_pending(request):

    profile = UserAdminProfile.objects.filter(
        user=request.user
    ).first()

    bookings = HotelBooking.objects.filter(
        profile=profile,
        status="Pending"
    )

    return render(
        request,
        "user_admin/hotel_bookings/hotel_booking_pending.html",
        {
            "bookings": bookings
        }
    )


@customer_only
def customer_dashboard(request):

    hotel_bookings = HotelBooking.objects.filter(
        customer_email=request.user.email
    )

    tour_bookings = Booking.objects.filter(
        customer_email=request.user.email
    )

    context = {

        "total_bookings": hotel_bookings.count() + tour_bookings.count(),

        "hotel_bookings": hotel_bookings.count(),

        "tour_bookings": tour_bookings.count(),

        "confirmed": (
            hotel_bookings.filter(status="Confirmed").count()
            +
            tour_bookings.filter(status="Confirmed").count()
        ),

        "pending": (
            hotel_bookings.filter(status="Pending").count()
            +
            tour_bookings.filter(status="Pending").count()
        ),

        "cancelled": (
            hotel_bookings.filter(status="Cancelled").count()
            +
            tour_bookings.filter(status="Cancelled").count()
        ),

    }

    return render(
        request,
        "customer/dashboard.html",
        context,
    )


@customer_only
def customer_hotel_bookings(request):

    bookings = HotelBooking.objects.filter(
        customer_email=request.user.email
    ).select_related(
        "hotel"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "customer/hotel_bookings.html",
        {
            "bookings": bookings
        }
    )


@customer_only
def customer_hotel_booking_detail(request, pk):

    booking = get_object_or_404(
        HotelBooking.objects.select_related(
            "hotel",
            "profile",
        ),
        id=pk,
        customer_email=request.user.email,
    )

    return render(
        request,
        "customer/hotel_booking_detail.html",
        {
            "booking": booking,
        }
    )


@customer_only
def customer_hotel_booking_cancel(request, pk):

    if request.method != "POST":
        return redirect(
            "customer_hotel_booking_detail",
            pk=pk
        )

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        customer_email=request.user.email,
    )

    # Already cancelled
    if booking.status == "Cancelled":

        messages.warning(
            request,
            "This booking is already cancelled."
        )

        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Payment protection
    if booking.payment_status == "Paid":

        messages.error(
            request,
            "This booking cannot be cancelled online because payment has already been completed."
        )

        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Only Pending / Confirmed bookings can be cancelled
    if booking.status not in ["Pending", "Confirmed"]:

        messages.error(
            request,
            "This booking cannot be cancelled."
        )

        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    booking.status = "Cancelled"

    booking.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Hotel booking cancelled successfully."
    )

    return redirect(
        "customer_hotel_booking_detail",
        pk=booking.id
    )       


@customer_only
def customer_tour_booking_detail(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "tour",
            "profile",
        ),
        id=pk,
        customer_email=request.user.email,
    )

    return render(
        request,
        "customer/tour_booking_detail.html",
        {
            "booking": booking,
        }
    )


@customer_only
def customer_tour_booking_cancel(request, pk):

    if request.method != "POST":
        return redirect(
            "customer_tour_booking_detail",
            pk=pk
        )

    booking = get_object_or_404(
        Booking,
        id=pk,
        customer_email=request.user.email,
    )

    # Already cancelled
    if booking.status == "Cancelled":

        messages.warning(
            request,
            "This tour booking is already cancelled."
        )

        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    # Payment protection
    if booking.payment_status == "Paid":

        messages.error(
            request,
            "This tour booking cannot be cancelled online because payment has already been completed."
        )

        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    # Only Pending / Confirmed bookings can be cancelled
    if booking.status not in ["Pending", "Confirmed"]:

        messages.error(
            request,
            "This tour booking cannot be cancelled."
        )

        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    # Cancel booking
    booking.status = "Cancelled"
    booking.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Tour booking cancelled successfully."
    )

    return redirect(
        "customer_tour_booking_detail",
        pk=booking.id
    )     


@customer_only
def customer_tour_bookings(request):

    bookings = Booking.objects.filter(
        customer_email=request.user.email
    ).select_related(
        "tour"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "customer/tour_bookings.html",
        {
            "bookings": bookings
        }
    )


@customer_only
def customer_wishlist_add(request):

    if request.method != "POST":
        return redirect("customer_dashboard")

    hotel_id = request.POST.get("hotel_id")
    tour_id = request.POST.get("tour_id")

    # -------------------------
    # HOTEL WISHLIST
    # -------------------------
    if hotel_id:

        hotel = get_object_or_404(
            Hotel,
            id=hotel_id,
            status=True
        )

        wishlist_item, created = CustomerWishlist.objects.get_or_create(
            user=request.user,
            hotel=hotel
        )

        if created:
            messages.success(
                request,
                f"{hotel.hotel_name} added to your wishlist."
            )
        else:
            messages.info(
                request,
                f"{hotel.hotel_name} is already in your wishlist."
            )

    # -------------------------
    # TOUR WISHLIST
    # -------------------------
    elif tour_id:

        tour = get_object_or_404(
            Tour,
            id=tour_id,
            status="Active"
        )

        wishlist_item, created = CustomerWishlist.objects.get_or_create(
            user=request.user,
            tour=tour
        )

        if created:
            messages.success(
                request,
                f"{tour.tour_name} added to your wishlist."
            )
        else:
            messages.info(
                request,
                f"{tour.tour_name} is already in your wishlist."
            )

    else:

        messages.error(
            request,
            "Invalid wishlist item."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "customer_dashboard"
        )
    )


@customer_only
def customer_wishlist_remove(request, pk):

    if request.method != "POST":
        return redirect("customer_wishlist")

    wishlist_item = get_object_or_404(
        CustomerWishlist,
        id=pk,
        user=request.user
    )

    wishlist_item.delete()

    messages.success(
        request,
        "Item removed from your wishlist."
    )

    return redirect("customer_wishlist")


@customer_only
def customer_wishlist(request):

    wishlist = CustomerWishlist.objects.filter(
        user=request.user
    ).select_related(
        "hotel",
        "tour"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "customer/wishlist.html",
        {
            "wishlist": wishlist
        }
    )




def customer_register(request):

    # If already logged in
    if request.user.is_authenticated:

        # Owner/Admin is currently logged in
        if hasattr(request.user, "admin_profile"):
            logout(request)

        # Customer is already logged in
        else:
            return redirect("customer_dashboard")

    form = CustomerRegisterForm()

    if request.method == "POST":

        form = CustomerRegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"].strip().lower()

            # Check existing user
            if User.objects.filter(
                username=email
            ).exists():

                messages.error(
                    request,
                    "This email is already registered. Please login."
                )

                return redirect(
                    "customer_login"
                )

            user = form.save(
                commit=False
            )

            user.username = email
            user.email = email

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            # Login newly registered customer
            login(request, user)

            messages.success(
                request,
                "Registration Successful."
            )

            return redirect(
                "customer_dashboard"
            )

    return render(
        request,
        "customer/register.html",
        {
            "form": form
        }
    )

def customer_login(request):

    # If already logged in
    if request.user.is_authenticated:

        # Owner/Admin is currently logged in
        if hasattr(request.user, "admin_profile"):
            logout(request)

        # Vendor is currently logged in
        elif getattr(request.user, "role", None) == "vendor":
            logout(request)

        # Customer is already logged in
        else:
            return redirect("customer_dashboard")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            # Owner/Admin account cannot login as Customer
            if hasattr(user, "admin_profile"):

                messages.error(
                    request,
                    "This is an Admin Panel account. Please use Admin Login."
                )

                return redirect("customer_login")

            # Vendor account cannot login as Customer
            if getattr(user, "role", None) == "vendor":

                messages.error(
                    request,
                    "This is a Vendor account. Please use Vendor Login."
                )

                return redirect("customer_login")

            # Clear previous session
            logout(request)

            # Login Customer
            login(request, user)

            messages.success(
                request,
                "Customer Login Successful."
            )

            return redirect(
                "customer_dashboard"
            )

        messages.error(
            request,
            "Invalid Email or Password."
        )

    return render(
        request,
        "customer/login.html"
    )

def customer_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged Out Successfully."
    )

    return redirect("home")


@customer_only
def customer_profile(request):

    user = request.user

    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()

        # -------------------------
        # VALIDATION
        # -------------------------

        if not email:
            messages.error(
                request,
                "Email address is required."
            )

            return redirect("customer_profile")

        # Check duplicate email
        if User.objects.filter(
            email=email
        ).exclude(
            id=user.id
        ).exists():

            messages.error(
                request,
                "This email is already registered."
            )

            return redirect("customer_profile")

        # -------------------------
        # UPDATE USER
        # -------------------------

        user.first_name = first_name
        user.last_name = last_name

        # Email is also used as username
        user.email = email
        user.username = email

        # Phone field
        user.phone = phone

        user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("customer_profile")

    return render(
        request,
        "customer/profile.html",
        {
            "user": user
        }
    )


@customer_only
def customer_settings(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Current password check
        if not request.user.check_password(current_password):
            messages.error(
                request,
                "Current password is incorrect."
            )
            return redirect("customer_settings")

        # Password length
        if len(new_password) < 8:
            messages.error(
                request,
                "New password must be at least 8 characters."
            )
            return redirect("customer_settings")

        # Confirm password
        if new_password != confirm_password:
            messages.error(
                request,
                "New passwords do not match."
            )
            return redirect("customer_settings")

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep customer logged in
        update_session_auth_hash(
            request,
            request.user
        )

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("customer_settings")

    return render(
        request,
        "customer/settings.html"
    )


@login_required
def customer_tour_booking_invoice(request, pk):

    booking = get_object_or_404(
        Booking,
        id=pk,
        customer_email=request.user.email
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Tour_Booking_{booking.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>TravelBiz</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Tour Booking Invoice",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Booking ID: #{booking.id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<br/>",
            styles["Normal"]
        )
    )

    data = [
        ["Booking ID", f"#{booking.id}"],

        ["Customer", booking.customer_name],

        ["Email", booking.customer_email],

        ["Phone", booking.customer_phone or "-"],

        ["Tour", booking.tour.tour_name],

        ["Location", booking.tour.location],

        ["Travel Date", str(booking.booking_date)],

        ["Persons", str(booking.persons)],

        ["Amount", f"₹ {booking.total_amount}"],

        ["Payment Status", booking.payment_status],

        ["Booking Status", booking.status],
    ]

    table = Table(
        data,
        colWidths=[
            2.2 * inch,
            3.5 * inch
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                "Helvetica"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    elements.append(table)

    elements.append(
        Paragraph(
            "<br/><b>Thank you for booking with TravelBiz.</b>",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return response    


@login_required
def customer_hotel_booking_invoice(request, pk):

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        customer_email=request.user.email
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Hotel_Booking_{booking.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    elements = []

    # -------------------------
    # HEADER
    # -------------------------

    elements.append(
        Paragraph(
            "<b>TravelBiz</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Hotel Booking Invoice",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # -------------------------
    # BOOKING INFORMATION
    # -------------------------

    data = [

        ["Booking ID", f"#{booking.id}"],

        [
            "Customer",
            booking.customer_name or "-"
        ],

        [
            "Email",
            booking.customer_email or "-"
        ],

        [
            "Phone",
            booking.customer_phone or "-"
        ],

        [
            "Hotel",
            booking.hotel.hotel_name
        ],

        [
            "Location",
            booking.hotel.location
        ],

        [
            "Check In",
            str(booking.check_in)
        ],

        [
            "Check Out",
            str(booking.check_out)
        ],

        [
            "Rooms",
            str(booking.rooms)
        ],

        [
            "Guests",
            str(booking.guests)
        ],

        [
            "Amount",
            f"Rs. {booking.total_amount}"
        ],

        [
            "Payment Status",
            booking.payment_status
        ],

        [
            "Booking Status",
            booking.status
        ],
    ]

    table = Table(
        data,
        colWidths=[
            2.2 * inch,
            3.5 * inch
        ]
    )

    table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                "Helvetica"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "<b>Thank you for booking with TravelBiz.</b>",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return response


@login_required
def customer_hotel_booking_invoice(request, pk):

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        customer_email=request.user.email
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Hotel_Booking_{booking.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    elements = []

    # -------------------------
    # HEADER
    # -------------------------

    elements.append(
        Paragraph(
            "<b>TravelBiz</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Hotel Booking Invoice",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # -------------------------
    # BOOKING INFORMATION
    # -------------------------

    data = [

        ["Booking ID", f"#{booking.id}"],

        [
            "Customer",
            booking.customer_name or "-"
        ],

        [
            "Email",
            booking.customer_email or "-"
        ],

        [
            "Phone",
            booking.customer_phone or "-"
        ],

        [
            "Hotel",
            booking.hotel.hotel_name
        ],

        [
            "Location",
            booking.hotel.location
        ],

        [
            "Check In",
            str(booking.check_in)
        ],

        [
            "Check Out",
            str(booking.check_out)
        ],

        [
            "Rooms",
            str(booking.rooms)
        ],

        [
            "Guests",
            str(booking.guests)
        ],

        [
            "Amount",
            f"Rs. {booking.total_amount}"
        ],

        [
            "Payment Status",
            booking.payment_status
        ],

        [
            "Booking Status",
            booking.status
        ],
    ]

    table = Table(
        data,
        colWidths=[
            2.2 * inch,
            3.5 * inch
        ]
    )

    table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                "Helvetica"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "<b>Thank you for booking with TravelBiz.</b>",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return response


@customer_only
def customer_tour_fake_payment(request, pk):

    booking = get_object_or_404(
        Booking,
        id=pk,
        customer_email=request.user.email
    )

    # Already paid
    if booking.payment_status == "Paid":
        messages.info(
            request,
            "This booking is already paid."
        )
        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    # Cancelled booking cannot be paid
    if booking.status == "Cancelled":
        messages.error(
            request,
            "Cancelled booking cannot be paid."
        )
        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    # Get or create payment
    payment, created = Payment.objects.get_or_create(
        tour_booking=booking,
        defaults={
            "merchant_order_id": (
                f"FAKE-TOUR-{booking.id}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            ),
            "amount": booking.total_amount,
            "status": "Pending",
        }
    )

    # Keep payment amount synced with booking amount
    if payment.amount != booking.total_amount:
        payment.amount = booking.total_amount
        payment.save(update_fields=["amount"])

    return render(
        request,
        "customer/fake_payment.html",
        {
            "booking": booking,
            "payment": payment,
            "payment_type": "Tour",
        }
    )

@customer_only
def customer_hotel_fake_payment(request, pk):

    booking = get_object_or_404(
        HotelBooking,
        id=pk,
        customer_email=request.user.email
    )

    # Already paid
    if booking.payment_status == "Paid":
        messages.info(
            request,
            "This booking is already paid."
        )
        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Cancelled booking cannot be paid
    if booking.status == "Cancelled":
        messages.error(
            request,
            "Cancelled booking cannot be paid."
        )
        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Get or create payment
    payment, created = Payment.objects.get_or_create(
        hotel_booking=booking,
        defaults={
            "merchant_order_id": (
                f"FAKE-HOTEL-{booking.id}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            ),
            "amount": booking.total_amount,
            "status": "Pending",
        }
    )

    # Keep payment amount synced with booking amount
    if payment.amount != booking.total_amount:
        payment.amount = booking.total_amount
        payment.save(update_fields=["amount"])

    return render(
        request,
        "customer/fake_payment.html",
        {
            "booking": booking,
            "payment": payment,
            "payment_type": "Hotel",
        }
    )



@customer_only
def fake_payment_success(request, pk):

    payment = get_object_or_404(
        Payment,
        id=pk
    )

    # Get related booking
    if payment.tour_booking:
        booking = payment.tour_booking

    elif payment.hotel_booking:
        booking = payment.hotel_booking

    else:
        messages.error(
            request,
            "Invalid payment."
        )
        return redirect("customer_dashboard")

    # Security: payment must belong to logged-in customer
    if booking.customer_email != request.user.email:
        messages.error(
            request,
            "You are not authorized to access this payment."
        )
        return redirect("customer_dashboard")

    # Already paid check
    if payment.status == "Success":
        messages.info(
            request,
            "This payment is already completed."
        )

        if payment.tour_booking:
            return redirect(
                "customer_tour_booking_detail",
                pk=booking.id
            )

        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Mark payment successful
    payment.status = "Success"
    payment.transaction_id = (
        f"FAKE-TXN-{uuid.uuid4().hex[:12].upper()}"
    )
    payment.save()

    # Mark booking as paid
    booking.payment_status = "Paid"
    booking.save()

    messages.success(
        request,
        "Payment successful."
    )

    # Redirect to correct booking detail
    if payment.tour_booking:
        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    return redirect(
        "customer_hotel_booking_detail",
        pk=booking.id
    )

@customer_only
def fake_payment_failed(request, pk):

    payment = get_object_or_404(
        Payment,
        id=pk
    )

    # Get related booking
    if payment.tour_booking:
        booking = payment.tour_booking

    elif payment.hotel_booking:
        booking = payment.hotel_booking

    else:
        messages.error(
            request,
            "Invalid payment."
        )
        return redirect("customer_dashboard")

    # Security: payment must belong to logged-in customer
    if booking.customer_email != request.user.email:
        messages.error(
            request,
            "You are not authorized to access this payment."
        )
        return redirect("customer_dashboard")

    # If payment is already successful,
    # don't allow it to become failed
    if payment.status == "Success":
        messages.info(
            request,
            "This payment has already been completed."
        )

        if payment.tour_booking:
            return redirect(
                "customer_tour_booking_detail",
                pk=booking.id
            )

        return redirect(
            "customer_hotel_booking_detail",
            pk=booking.id
        )

    # Mark payment as failed
    payment.status = "Failed"
    payment.save()

    # Keep booking payment status pending
    booking.payment_status = "Pending"
    booking.save()

    messages.error(
        request,
        "Payment failed. Please try again."
    )

    # Redirect to correct booking detail
    if payment.tour_booking:
        return redirect(
            "customer_tour_booking_detail",
            pk=booking.id
        )

    return redirect(
        "customer_hotel_booking_detail",
        pk=booking.id
    )
            