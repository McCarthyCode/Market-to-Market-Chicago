from django.shortcuts import render, redirect
from django.http import (
    HttpResponseBadRequest,
    # HttpResponseNotFound,
    # HttpResponseRedirect,
    # JsonResponse,
)

def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    return redirect('users:index')
