from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from PIL import Image
from colorthief import ColorThief
from tempfile import NamedTemporaryFile

import json
import base64

# Create your views here.


def naive_proc_img(filename):
    image = Image.open(filename)
    width, height = image.size
    middle = width // 2
    top = height * 0.33333
    bottom = height * 0.88
    return image.getpixel((middle, top)), image.getpixel((middle, bottom)), width, height


def naive_upload_image(request):
    f = request.FILES['image']
    dest = NamedTemporaryFile('wb+')
    for chunk in f.chunks():
        dest.write(chunk)
    top, bottom, width, height = naive_proc_img(dest.name)
    img = base64.b64encode(open(dest.name, 'rb').read())
    return HttpResponse(json.dumps({'jane': 'success', 'top': str(top), 'bottom': str(bottom), 'pic': img.decode('ascii'), 'width': width, 'height': height}), content_type='application/json')


def proc_img(filename):
    image = ColorThief(filename)
    return image.get_palette(quality=1)


def upload_image(request):
    f = request.FILES['image']
    dest = NamedTemporaryFile('wb+')
    for chunk in f.chunks():
        dest.write(chunk)
    colors = [str(c) for c in proc_img(dest.name)]
    img = base64.b64encode(open(dest.name, 'rb').read())
    return HttpResponse(json.dumps({'jane': 'success', 'colors': colors, 'pic': img.decode('ascii')}), content_type='application/json')

