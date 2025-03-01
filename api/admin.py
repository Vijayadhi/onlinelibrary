from django.contrib import admin

# Register your models here.
from api.models import UploadBookImage


class UploadBookImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'img_tag')

admin.site.register(UploadBookImage, UploadBookImageAdmin)