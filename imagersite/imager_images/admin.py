from django.contrib import admin
from imager_images.models import Photo

# Register your models here.

class PhotoAdmin(admin.ModelAdmin):

    list_display = ('title')
    list_filter = ('title')


admin.site.register(Photo, PhotoAdmin)
