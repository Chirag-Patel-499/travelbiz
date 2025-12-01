from django.contrib import admin
from .models import HeroSection, Category, Destination, MiddleBanner, Deal, CallSection, FooterQuickLink, FooterCategory, FooterContact, SocialLink

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", )


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