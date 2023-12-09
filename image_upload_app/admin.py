from django.contrib import admin
from .models import CustomUser, Image, AccountTier, ExpiringLink


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'account_tier')
    list_editable = ('account_tier',)
    list_display_links = ('id', 'username')


class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at')
    list_display_links = ('id', 'user')


class ExpiringLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'token', 'expiration_date', 'is_expired')
    list_display_links = ('id', 'image')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(ExpiringLink, ExpiringLinkAdmin)

admin.site.site_header = 'Image Upload Admin Panel'
admin.site.site_title = 'Image Upload App'
admin.site.index_title = 'Administration'
