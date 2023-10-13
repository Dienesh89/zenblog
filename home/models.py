from django.db import models
# importing ResizedImageField for resized image
from django_resized import ResizedImageField
# for custom user
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import customUserManager
# form making the slug
from autoslug import AutoSlugField

# Contact model
class Contact(models.Model):
    name = models.CharField(max_length=20) 
    email = models.EmailField(max_length=20)
    subj = models.TextField() 
    msg = models.TextField()
    date = models.DateField()

# customuser model
class customuser(AbstractUser):
	
	first_name = None
	last_name = None
	
	username = models.CharField(max_length=20)
	email = models.EmailField(_("email_address"),unique=True)
	
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []
	
	objects = customUserManager()
	
	def __str__(self):
		return self.email

# model for the profile picture of the user
class ProfPic(models.Model):
    Unique_id = models.AutoField(primary_key=True)
    pic = ResizedImageField(size=[150,150] , upload_to="profile_pics",default="profile_pics/default.svg")
    user = models.OneToOneField(customuser,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Profile picture of {self.user}"

# model for the information of post
class postInfo(models.Model):
    id = models.AutoField(primary_key=True)
    slug = AutoSlugField(populate_from="title",unique=True)
    thumbnail = models.ImageField(upload_to="post_thumbnails",default="post_thumbnails/island.png")
    title = models.CharField(max_length=20)
    desc = models.TextField()
    user = models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    category = models.CharField(max_length=20,default="No Category")
    date = models.DateField(auto_now_add=True)
    htmlCode = models.TextField(default="Nothing")
    post_views = models.IntegerField(default=0)


class postImages(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='post_content_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
