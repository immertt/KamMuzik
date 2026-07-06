from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.")
            return redirect("contact:contact")
        else:
            messages.error(request, "Lütfen formu kontrol edin, bazı alanlar hatalı.")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})