from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """ContactMessage modelinden otomatik form üretir."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Adınız Soyadınız",
                "class": "form__input",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "ornek@eposta.com",
                "class": "form__input",
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Konu (isteğe bağlı)",
                "class": "form__input",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Mesajınız...",
                "class": "form__input",
                "rows": 5,
            }),
        }