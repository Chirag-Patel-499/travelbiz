from django import forms
from main.models import Vendor

class VendorRegisterForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            "business_name",
            "tagline",
            "description",
            "address",
            "city",
            "state",
            "country",
            "gst_number",
            "logo",
        ]
