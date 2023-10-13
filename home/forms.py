from django import forms
from .models import ProfPic,postInfo
from django.forms import FileInput

# form for profile picture
class ProfPicForm(forms.ModelForm):
    class Meta:
        model = ProfPic
        fields = ["Unique_id","pic"]
        labels = {"pic":"Profile pic"}
        widgets = {
            'pic': FileInput(attrs={
                'class': "custom-file-input form-control",
                })
        }

# form for the thumbnail of the post
class postInfoForm(forms.ModelForm):
    class Meta:
        model = postInfo
        fields = ["thumbnail"]
        labels = {"thumbnail":"Thumbnail"}
        widgets = {
            'thumbnail': FileInput(attrs={
                'class': "custom-file-input form-control",
                'id':'post-thumbnail'
                })
        }