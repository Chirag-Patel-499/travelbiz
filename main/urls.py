from django import views
from django.urls import path
from .views import (
    customer_tour_bookings,
    customer_hotel_bookings,
    customer_register,
    customer_login,
    customer_logout,
    customer_dashboard,
    customer_wishlist,
    customer_wishlist_add,
    customer_wishlist_remove,
    hotel_booking,
    hotel_booking_pending,
    hotel_booking_list,
    hotel_booking_view,
    hotel_booking_confirm,
    hotel_booking_cancel,
    hotel_booking_confirmed,
    hotel_booking_cancelled,
    hotel_detail,
    booking_cancel,
    booking_confirm,
    booking_invoice,
    home,
    hotel_image_delete,
    tour_booking,
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
    tour_detail,

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
    "tour/<int:pk>/",
    tour_detail,
    name="tour_detail",
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

    path(
    "tour/<int:pk>/booking/",
    tour_booking,
    name="tour_booking",
    ),

    path(
    "dashboard/bookings/invoice/<int:pk>/",
    booking_invoice,
    name="booking_invoice",
    ),


        # -----------------------------------
    # Hotel Bookings
    # -----------------------------------

    path(
        "dashboard/hotel-bookings/",
        hotel_booking_list,
        name="hotel_booking_list",
    ),

    path(
        "dashboard/hotel-bookings/view/<int:pk>/",
        hotel_booking_view,
        name="hotel_booking_view",
    ),

    path(
        "dashboard/hotel-bookings/confirm/<int:pk>/",
        hotel_booking_confirm,
        name="hotel_booking_confirm",
    ),

    path(
        "dashboard/hotel-bookings/cancel/<int:pk>/",
        hotel_booking_cancel,
        name="hotel_booking_cancel",
    ),

    path(
        "dashboard/hotel-bookings/confirmed/",
        hotel_booking_confirmed,
        name="hotel_booking_confirmed",
    ),

    path(
        "dashboard/hotel-bookings/cancelled/",
        hotel_booking_cancelled,
        name="hotel_booking_cancelled",
    ),

    path(
    "hotel/<int:pk>/",
    hotel_detail,
    name="hotel_detail",
    ),

    path(
    "hotel/<int:pk>/booking/",
    hotel_booking,
    name="hotel_booking",
    ),

    path(
    "dashboard/hotel-bookings/pending/",
    hotel_booking_pending,
    name="hotel_booking_pending",
    ),

    path(
    "customer/dashboard/",
    customer_dashboard,
    name="customer_dashboard",
    ),

    path(
    "customer/register/",
    customer_register,
    name="customer_register"
    ),


    path(
    "customer/login/",
    customer_login,
    name="customer_login",
    ),

    path(
        "customer/logout/",
        customer_logout,
        name="customer_logout",
    ),

    path(
    "customer/hotel-bookings/",
    customer_hotel_bookings,
    name="customer_hotel_bookings",
    ),

    path(
    "customer/tour-bookings/",
    customer_tour_bookings,
    name="customer_tour_bookings",
    ),

    # =========================
    # CUSTOMER WISHLIST
    # =========================

    path(
        "customer/wishlist/",
        customer_wishlist,
        name="customer_wishlist",
    ),

    path(
        "customer/wishlist/add/",
        customer_wishlist_add,
        name="customer_wishlist_add",
    ),

    path(
        "customer/wishlist/remove/<int:pk>/",
        customer_wishlist_remove,
        name="customer_wishlist_remove",
    ),

    

]
