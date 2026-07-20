from django import views
from django.urls import path
from .views import (
    booking_cancel,
    booking_confirm,
    home,
    hotel_image_delete,
    tour_image_delete,
    tour_images,
    tour_delete,
    tour_edit,
    tour_view,
    tour_add,
    tour_list,
    user_logout,
    vendor_register,
    vendor_login,
    vendor_dashboard,
    vendor_success,
    blog_list,
    blog_detail,
    contact_page,
    wishlist_page,
    become_driver,
    my_account,
    help_page,
    search_results,
    user_admin_login,
    user_admin_register,
    user_dashboard,
    user_logout,
    hotel_list,
    hotel_add,
    hotel_images,
    hotel_view,
    hotel_edit,
    hotel_delete,
    booking_list,
    booking_view,
    booking_pending,
    booking_confirmed,
    booking_cancelled,

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

    path("wishlist/", wishlist_page, name="wishlist"),
    
    # urls.py
    path('become-driver/', become_driver, name='become_driver'),

    path("my-account/", my_account, name="my_account"),

    path("help/", help_page, name="help"),

    path("search/", search_results, name="search_results"),

    # User Admin Login
    path(
        "create-admin/",
        user_admin_login,
        name="user_admin_login",
    ),

    # User Admin Register
    path(
        "create-admin/register/",
        user_admin_register,
        name="user_admin_register",
    ),

    # Dashboard
    path(
        "dashboard/",
        user_dashboard,
        name="user_dashboard",
    ),

    # Logout
    path(
        "logout/",
        user_logout,
        name="user_logout",
    ),

    # Hotels

    path(
        "dashboard/hotels/",
        hotel_list,
        name="hotel_list",
    ),

    path(
        "dashboard/hotels/add/",
        hotel_add,
        name="hotel_add",
    ),

    path(
        "dashboard/hotels/images/",
        hotel_images,
        name="hotel_images",
    ),


    path(
        "dashboard/hotels/view/<int:id>/",
        hotel_view,
        name="hotel_view",
    ),

    path(
        "dashboard/hotels/edit/<int:id>/",
        hotel_edit,
        name="hotel_edit",
    ),

    path(
        "dashboard/hotels/delete/<int:id>/",
        hotel_delete,
        name="hotel_delete",
    ),

    path(
        "dashboard/hotels/images/delete/<int:id>/",
        hotel_image_delete,
        name="hotel_image_delete",
    ),

    path(
    "dashboard/tours/",
    tour_list,
    name="tour_list",
    ),

    path(
    "dashboard/tours/add/",
    tour_add,
    name="tour_add",
    ),

    path(
    "dashboard/tours/view/<int:pk>/",
    tour_view,
    name="tour_view",
    ),

    path(
    "dashboard/tours/edit/<int:pk>/",
    tour_edit,
    name="tour_edit",
    ),

    path(
    "dashboard/tours/delete/<int:pk>/",
    tour_delete,
    name="tour_delete",
    ),

    path(
    "dashboard/tours/images/",
    tour_images,
    name="tour_images",
    ),

    path(
    "dashboard/tours/images/delete/<int:pk>/",
    tour_image_delete,
    name="tour_image_delete",
    ),

    path(
    "dashboard/bookings/",
    booking_list,
    name="booking_list",
    ),

    path(
        "dashboard/bookings/view/<int:pk>/",
        booking_view,
        name="booking_view",
    ),

    path(
        "dashboard/bookings/pending/",
        booking_pending,
        name="booking_pending",
    ),

    path(
    "dashboard/bookings/confirm/<int:pk>/",
    booking_confirm,
    name="booking_confirm",
    ),

    path(
        "dashboard/bookings/cancel/<int:pk>/",
        booking_cancel,
        name="booking_cancel",
    ),

    path(
        "dashboard/bookings/confirmed/",
        booking_confirmed,
        name="booking_confirmed",
    ),

    path(
        "dashboard/bookings/cancelled/",
        booking_cancelled,
        name="booking_cancelled",
    ),

    

]
