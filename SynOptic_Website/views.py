from django.shortcuts import render, HttpResponse, redirect
from .AudioizationScripts.image_to_sound import image_to_audio
from tempfile import NamedTemporaryFile
from .forms import *
import io
import PIL
import os
from django.core.files.uploadedfile import InMemoryUploadedFile


def index(request):
    if request.method == 'POST':
        form = MIDIConfig(request.POST, request.FILES)
        if form.is_valid():
            ### Algorithm: Resize image, run image through audioization algorithm,
            ### save file data to temporary variable, send data back to user as attachment

            # Get uploaded image, resize it, then
            originalImage = form.cleaned_data['image']
            fileName = form.cleaned_data['fileName']
            size = int(form.cleaned_data['length'])
            pilImg = PIL.Image.open(originalImage)
            pilImg = pilImg.resize((size, size))
            img_io = io.BytesIO()
            fileType = os.path.splitext(originalImage.name)[1].upper().replace('.', '')
            if (fileType == "JPG"):
                fileType = "JPEG"
            print(fileType)
            pilImg.save(img_io, format=fileType)

            # Create a new Django file-like object to be the resized image
            resizedImage = InMemoryUploadedFile(img_io, None, 'foo.jpg', 'image/jpeg',
                                                img_io.tell(), None)

            choice = form.cleaned_data['scale']
            scale, scaleName = get_scale(choice)

            # Write generated MIDI binary data to temporary file then read the contents into a variable
            # This is done because the MIDIUtil library can only export by writing to a file
            with NamedTemporaryFile(mode='rb+') as temp:
                midi = image_to_audio(resizedImage, scale, 8)
                midi.writeFile(temp)
                temp.flush()
                temp.seek(0)
                fileContents = temp.read()

            # Create and send http file attachment response
            response = HttpResponse(fileContents)
            response[
                'Content-Disposition'] = 'attachment; filename=' + fileName + '.mid'  # originalImage.name.split('.')[0] + "in" + scaleName + '.mid'
            return response
        else:
            return render(request, "SynOptic_Website/index.html", {'form': form})
    else:
        form = MIDIConfig()
        return render(request, 'SynOptic_Website/index.html', {'form': form})


def get_scale(choice):
    cMajor_scale = [72, 74, 76, 77, 79, 81, 83, 84]
    aMinor_scale = [67, 69, 70, 72, 74, 75, 77, 79]
    cMaj_Pent_Scale = [72, 70, 78, 12, 81, 87, 14, 10]
    # cMaj_Pent_Scale = [72,74,76,79,81,84]
    if choice == "CMAJOR":
        return (cMajor_scale, "Cmajor")
    elif choice == "AMINOR":
        return (aMinor_scale, "Aminor")
    else:
        return (cMaj_Pent_Scale, "CmajorPent")

