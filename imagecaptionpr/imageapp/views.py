from django.shortcuts import render
from .forms import ImageUploadForm
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the processor and model once to avoid reloading them on each request
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(request):
    caption = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            image_instance = form.save()

            # Load the image
            image_path = image_instance.image.path
            image = Image.open(image_path)

            # Prepare the image
            inputs = processor(image, return_tensors="pt")

            # Generate captions
            outputs = model.generate(**inputs)
            caption = processor.decode(outputs[0], skip_special_tokens=True)

            # Update the caption in the database (if using a model)
            image_instance.caption = caption
            image_instance.save()

    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'form': form, 'caption': caption})

