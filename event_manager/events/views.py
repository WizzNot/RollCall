from django.shortcuts import render


def add_event(request):
    return render(request, 'events/main.html')
