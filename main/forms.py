from django import forms
from main.models import Vendor

from .models import UserAdminProfile

from .models import Hotel

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
    


class HotelForm(forms.ModelForm):

    class Meta:

        model = Hotel

        exclude = ["profile"]

        widgets = {

            "hotel_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Hotel Name"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Hotel Location"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter Hotel Address"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write Hotel Description"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Price Per Night",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "total_rooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Total Rooms",
                    "min": "1"
                }
            ),

            "status": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }