from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from colorthief import ColorThief
from tempfile import NamedTemporaryFile

import json
import base64

# Create your views here.


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

