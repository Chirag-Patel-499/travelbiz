from django.contrib import admin
from .models import HeroSection, Category, Destination, MiddleBanner, Deal,CallSection,FooterQuickLink, FooterCategory, FooterContact, SocialLink, Vendor, VendorDocument, Blog, BlogCategory, ContactPage, Wishlist, WishlistBanner, DriverApplication

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)

    fieldsets = (
        ("Hero Content", {
            "fields": ("title", "subtitle")
        }),
        ("Hero Video", {
            "fields": ("background_video",),
            "description": "MP4 video only. This will be used as hero background."
        }),
        ("Search Bar", {
            "fields": ("search_placeholder_1", "search_placeholder_2")
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "count", "price_text")



@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("title", "country_category", "rating")


@admin.register(MiddleBanner)
class MiddleBannerAdmin(admin.ModelAdmin):
    list_display = ("main_title",)    


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "rating", "discount")


@admin.register(CallSection)
class CallSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(FooterQuickLink)
class FooterQuickLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url")


@admin.register(FooterCategory)
class FooterCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "url")


@admin.register(FooterContact)
class FooterContactAdmin(admin.ModelAdmin):
    list_display = ("address", "phone", "email")    


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url")    




class VendorDocumentInline(admin.TabularInline):
    model = VendorDocument
    extra = 1


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "phone", "verified", "status", "city", "country")
    list_filter = ("verified", "status", "country")
    search_fields = ("business_name", "user__username", "phone")
    inlines = [VendorDocumentInline]

    @admin.action(description="Approve Selected Vendors")
    def approve_vendors(self, request, queryset):
        queryset.update(verified=True, status="active")

    @admin.action(description="Mark Selected Vendors as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(status="inactive")

    @admin.action(description="Block Selected Vendors")
    def block_vendors(self, request, queryset):
        queryset.update(status="blocked")

    actions = ["approve_vendors", "make_inactive", "block_vendors"]



@admin.register(VendorDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = ("vendor", "document_type", "approved", "uploaded_at")
    list_filter = ("approved", "document_type")
    search_fields = ("vendor__business_name", "document_type")    


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at", "views")
    list_filter = ("category", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}




@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "rating", "discount")
    search_fields = ("title", "location", "category")
    list_filter = ("category", "rating")    


@admin.register(WishlistBanner)
class WishlistBannerAdmin(admin.ModelAdmin):
    list_display = ("title",)    


@admin.register(DriverApplication)
class DriverApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "city",
        "vehicle_type",
        "phone",
        "created_at",
    )
    search_fields = ("full_name", "phone", "city")
    list_filter = ("city", "vehicle_type")    