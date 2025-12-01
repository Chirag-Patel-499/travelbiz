from django.shortcuts import render
from .models import HeroSection, Category, Destination, MiddleBanner, Deal, CallSection, FooterQuickLink, FooterCategory, FooterContact, SocialLink

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






    }
    return render(request, "index.html", context)
