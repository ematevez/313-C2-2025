from django.shortcuts import render


def juego_in(request):
    return render(request, "dashboard.html")
