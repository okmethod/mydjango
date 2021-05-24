from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

def index(request):
    return render(request, 'index/index.html')
