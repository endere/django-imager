from django.contrib import admin
from imager_images.models import Photo, Album

# Register your models here.

# admin.site.register(Photo)
admin.site.register(Album)


class PhotoAdmin(admin.ModelAdmin):

    list_display = ('title',)
    # list_filter = ('title')

admin.site.register(Photo, PhotoAdmin)
