from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

def top_page(request):
    return render(request, 'top_page/top_page.html')
