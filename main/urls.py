from django.urls import path
from .views import (
    home,
    vendor_register,
    vendor_login,
    vendor_dashboard,
    vendor_success,
    blog_list,
    blog_detail,
    contact_page,

)

urlpatterns = [
    path("", home, name="home"),

    # Vendor Registration
    path("register-vendor/", vendor_register, name="vendor_register"),

    # Vendor Login
    path("vendor-login/", vendor_login, name="vendor_login"),

    # Vendor Dashboard
    path("vendor-dashboard/", vendor_dashboard, name="vendor_dashboard"),

    # Vendor Success
    path("vendor-success/", vendor_success, name="vendor_success"),
    
    # BLOG PAGE
    path("blog/", blog_list, name="blog_list"),
    path("blog/<slug:slug>/", blog_detail, name="blog_detail"),

    path('contact/', contact_page, name='contact'),



]
