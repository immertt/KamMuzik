from django.contrib import admin
from .models import ContactMessage
from django.contrib.auth.models import User, Group
from django.utils.html import format_html


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["durum", "name", "email", "subject", "created_at"]
    list_display_links = ["name"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]
    list_per_page = 30
    ordering = ["-created_at"]
    actions = ["okundu_isaretle", "okunmadi_isaretle"]

    fieldsets = [
        ("Gönderen", {
            "fields": ["name", "email"]
        }),
        ("Mesaj", {
            "fields": ["subject", "message", "created_at"]
        }),
        ("Durum", {
            "fields": ["is_read"]
        }),
    ]

    def durum(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#6B7B8C;">● Okundu</span>')
        return format_html('<span style="color:#5DA9F0;font-weight:600;">● Yeni</span>')
    durum.short_description = "Durum"

    def has_add_permission(self, request):
        return False  # mesajlar sadece formdan gelir

    @admin.action(description="Seçili mesajları okundu işaretle")
    def okundu_isaretle(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} mesaj okundu olarak işaretlendi.")

    @admin.action(description="Seçili mesajları okunmadı işaretle")
    def okunmadi_isaretle(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} mesaj okunmadı olarak işaretlendi.")
    
admin.site.unregister(User)
admin.site.unregister(Group)