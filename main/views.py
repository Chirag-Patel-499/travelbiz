from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import (
    HeroSection, Category, Destination, MiddleBanner, Deal,
    CallSection, FooterQuickLink, FooterCategory, FooterContact,
    SocialLink, Vendor, Blog, BlogCategory
)

from main.forms import VendorRegisterForm
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
    }
    return render(request, "index.html", context)



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
@login_required
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
