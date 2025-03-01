from django.db import models

# Create your models here.
from django.utils.html import format_html


class UploadBookImage(models.Model):
    image = models.ImageField(upload_to='media', blank=True, null=True)

    def img_tag(self):
        return format_html('<img href="{0}" src="{0}" width="150" height="150" />'.format(self.image.url))

    img_tag.allow_tags = True

