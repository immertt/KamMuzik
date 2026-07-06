from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django.core.mail import EmailMessage
from pages.models import SiteContent


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Arkadaşına bildirim e-postası gönder
            try:
                email = EmailMessage(
                    subject=f"Yeni İletişim Mesajı: {contact_message.subject or 'Konusuz'}",
                    body=(
                        f"Gönderen: {contact_message.name}\n"
                        f"E-posta: {contact_message.email}\n"
                        f"Konu: {contact_message.subject or '—'}\n\n"
                        f"Mesaj:\n{contact_message.message}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    to=[SiteContent.load().contact_email],
                    reply_to=[contact_message.email],
                )
                email.send(fail_silently=True)
            except Exception:
                pass  # e-posta gitmese bile mesaj veritabanına kaydedildi

            messages.success(request, "Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.")
            return redirect("contact:contact")
        else:
            messages.error(request, "Lütfen formu kontrol edin, bazı alanlar hatalı.")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})