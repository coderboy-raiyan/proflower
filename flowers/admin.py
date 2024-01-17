from django.contrib import admin
from .models import FlowerModel, ReviewModel, CategoryModel
# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


admin.site.register(FlowerModel)
admin.site.register(ReviewModel)
admin.site.register(CategoryModel, CategoryModelAdmin)
