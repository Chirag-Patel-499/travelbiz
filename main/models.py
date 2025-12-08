from django.db import models
from django.conf import settings
from django.utils.text import slugify


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




def vendor_logo_upload(instance, filename):
    return f"vendors/logos/{instance.user.username}/{filename}"

def vendor_document_upload(instance, filename):
    return f"vendors/documents/{instance.vendor.user.username}/{filename}"


class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_profile"
    )

    business_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=vendor_logo_upload, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True) 
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=50, blank=True, null=True)

    verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("blocked", "Blocked")
        ],
        default="inactive"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


class VendorDocument(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to=vendor_document_upload)
    approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vendor Document"
        verbose_name_plural = "Vendor Documents"

    def __str__(self):
        return f"{self.document_type} - {self.vendor.business_name}"
    



class BlogCategory(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to="blogs/")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, default="Admin")
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title    
    

class ContactPage(models.Model):
    hero_title = models.CharField(max_length=255, default="Contact TravelBiz")
    hero_subtitle = models.CharField(max_length=255, blank=True, null=True)
    hero_image = models.ImageField(upload_to="contact/", blank=True, null=True)

    help_center_title = models.CharField(max_length=255, default="Help Center")
    help_center_phone = models.CharField(max_length=50, blank=True, null=True)
    help_center_email = models.CharField(max_length=100, blank=True, null=True)

    address_title = models.CharField(max_length=255, default="Address")
    address_text = models.CharField(max_length=255, blank=True, null=True)

    business_title = models.CharField(max_length=255, default="Business Queries")
    business_phone = models.CharField(max_length=50, blank=True, null=True)
    business_email = models.CharField(max_length=100, blank=True, null=True)

    map_embed_url = models.TextField(
        blank=True,
        null=True,
        help_text="Paste the Google Maps Embed URL here"
    )

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page Settings"

    def __str__(self):
        return "Contact Page Settings"

