from django.contrib import admin
from .models import CustomerModel, TokenModel
# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(TokenModel)
