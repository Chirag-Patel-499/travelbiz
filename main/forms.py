from django import forms
from main.models import Vendor

from .models import UserAdminProfile

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


class UserAdminRegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:

        model = UserAdminProfile

        fields = [
            "company_name",
            "owner_name",
            "email",
            "mobile",
            "business_type",
            "country",
            "state",
            "city",
            "logo",
        ]

    def clean(self):

        cleaned = super().clean()

        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")

        return cleaned