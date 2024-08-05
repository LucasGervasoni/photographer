# from django import forms
# from .models import File

# class ImageForm(forms.ModelForm):
#   photo = forms.FileField(widget = forms.TextInput(attrs={
#             "name": "images",
#             "type": "File",
#             "class": "form-control align-self-center w-50 formFiles ml-auto mr-auto",
#             "multiple": "True",
#         }))
#   editor_notes = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
#   class Meta:
#     model = File
#     fields = '__all__'