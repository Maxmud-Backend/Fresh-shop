from django.contrib import admin

from shop.models import CustomUser, Contact, Category, SubCategory, Product, Gallery, Like, Comment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(SubCategory)
class GalleryAdmin(admin.TabularInline):
    model = Gallery
    fk_name = "product"
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [GalleryAdmin]
admin.site.register(Product,ProductAdmin)
admin.site.register(Like)
admin.site.register(Comment)


