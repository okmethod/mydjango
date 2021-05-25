from django.shortcuts import render

def reversi(request):
    return render(request, 'reversi/reversi.html')
