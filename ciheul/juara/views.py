from django.shortcuts import render


def home(request):
    context = {
        'title_head': 'Bandung Juara!',
        'title': 'Bandung Juara!',
    }
    return render(request, "base_juara.html", context)
