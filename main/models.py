from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    background_image = models.ImageField(upload_to="hero/")
    search_placeholder_1 = models.CharField(max_length=255, default="Where do you want to go?")
    search_placeholder_2 = models.CharField(max_length=255, default="Dates / flexible")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return self.title
    


class Category(models.Model):
    title = models.CharField(max_length=100)          # Beaches, Mountains
    count = models.PositiveIntegerField()             # 120
    price_text = models.CharField(max_length=100)     # From ₹2,999
    icon_class = models.CharField(max_length=100)     # icon-sun, icon-mountain
    url = models.CharField(max_length=255, default="#")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title




class Destination(models.Model):
    ribbon_text = models.CharField(max_length=50, blank=True, null=True)  # Best Seller, Hot, New
    image = models.ImageField(upload_to="destinations/")
    country_category = models.CharField(max_length=255)  # Beach · India
    title = models.CharField(max_length=255)  # Goa Beaches
    price_text = models.CharField(max_length=255)  # Starts from ₹2,999
    open_text = models.CharField(max_length=50)  # Open All Year / Seasonal
    reviews_text = models.CharField(max_length=255)  # 5200 Reviews
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 9.2
    

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.title
    

class MiddleBanner(models.Model):
    small_title = models.CharField(max_length=255, blank=True, null=True)
    main_title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    button_text = models.CharField(max_length=100)
    button_url = models.CharField(max_length=255, default="#")
    background_image = models.ImageField(upload_to="middle_banner/")

    class Meta:
        verbose_name = "Middle Banner"
        verbose_name_plural = "Middle Banner"

    def __str__(self):
        return self.main_title


class Deal(models.Model):
    image = models.ImageField(upload_to="deals/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 9.5
    category = models.CharField(max_length=255)  # Family · Goa
    title = models.CharField(max_length=255)  # Goa Family Pack
    subtitle = models.CharField(max_length=255)  # 3 nights · From ₹9,999
    discount = models.CharField(max_length=50, blank=True, null=True)  # -20%
    person_type = models.CharField(max_length=50)  # Per person / Per couple
    url = models.CharField(max_length=255, default="#")

    class Meta:
        verbose_name = "Deal"
        verbose_name_plural = "Deals"

    def __str__(self):
        return self.title



class CallSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    button_text = models.CharField(max_length=100)
    button_url = models.CharField(max_length=255, default="#")
    background_image = models.ImageField(upload_to="call_section/")

    class Meta:
        verbose_name = "Call Section"
        verbose_name_plural = "Call Section"

    def __str__(self):
        return self.title



class FooterQuickLink(models.Model):
    title = models.CharField(max_length=100)   # Become a Partner
    url = models.CharField(max_length=255)     # /submit-trip/ or #
    
    class Meta:
        verbose_name = "Footer Quick Link"
        verbose_name_plural = "Footer Quick Links"

    def __str__(self):
        return self.title



class FooterCategory(models.Model):
    title = models.CharField(max_length=100)   # Top Categories, Best Deals
    url = models.CharField(max_length=255)     # /categories/top/ or #
    
    class Meta:
        verbose_name = "Footer Category"
        verbose_name_plural = "Footer Categories"

    def __str__(self):
        return self.title



class FooterContact(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Footer Contact"
        verbose_name_plural = "Footer Contact"

    def __str__(self):
        return "Footer Contact Information"



class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter / X"),
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("whatsapp", "WhatsApp"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    icon_class = models.CharField(max_length=50)   # bi bi-facebook, bi bi-instagram
    url = models.CharField(max_length=255)         # https://facebook.com/

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.platform
