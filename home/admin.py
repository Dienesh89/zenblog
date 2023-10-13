from django.contrib import admin
from home.models import Contact , customuser , ProfPic , postInfo,postImages

# Register your models here.
admin.site.register([
    Contact,
    customuser,
    ProfPic,
    postInfo,
    postImages,
])

class ProfPicAdmin(admin.ModelAdmin):
    list_display = ["id","pic"]