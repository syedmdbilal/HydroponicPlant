from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from employee.forms import EmployeeForm

from django.views.generic import DetailView
from employee.models import Employee

from keras.models import load_model
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

class EmployeeImage(TemplateView):
    form = EmployeeForm
    template_name = 'emp_image.html'

    def post(self, request, *args, **kwargs):
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()

            return HttpResponseRedirect(reverse_lazy('emp_image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EmpImageDisplay(DetailView):
    model = Employee
    template_name = 'emp_image_display.html'
    context_object_name = 'emp'


def nail(request):
    result1 = Employee.objects.latest('id')
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    import h5py
    models = keras.models.load_model('C:/Users/SMB/Desktop/Hydroponic Plant/Deploy/employee/LeNet.h5')

    from tensorflow.keras.preprocessing import image
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open("C:/Users/SPIRO-PYTHON1/Desktop/Hydroponic Plant/Deploy/media/" + str(result1)).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    classes = ['Apple Black Rot',
               'Apple Cedar Apple Rust',
               'Apple Healthy',
               'Apple Powdery Mildew',
               'Apple Scab',
               'Pepper Bell Bacterial Spot',
               'Pepper Bell Healthy',
               'Tomato Bacterial Spot',
               'Tomato Early Blight',
               'Tomato Healthy',
               'Tomato Late Blight',
               'Tomato Leaf Mold']

    prediction = models.predict(data)
    idd = np.argmax(prediction)
    a = (classes[idd])
    return render(request, "result.html", {"out": a})
