from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


def error_404(request):

    contexts = {
        'request_path': request.path,
    }

    return render(request, '404.html', contexts, status=404)
