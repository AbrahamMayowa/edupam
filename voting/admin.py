from django.contrib import admin
from .models import Award, Contestant, Category

admin.site.register(Award)
admin.site.register(Category)
admin.site.register(Contestant)
# Register your models here.
