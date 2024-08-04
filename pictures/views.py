from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Image


# Create your views here.
def uploadPage(request):
  form = ImageForm(request.POST, request.FILES)
  if request.method == "POST":
    images = request.FILES.getlist('photo')
    for image in images:
          image_ins = Image(photo = image)
          image_ins.save()
          
    return redirect('listImages')
  
  context = {'form': form} 
  return render(request, 'uploadPage.html', context)

def listImages(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, "uploadPage.html", context)