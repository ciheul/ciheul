from django.shortcuts import render


def home(request):
    context = {
        'title_head': 'Dirban - Direktori Bandung',
        'title': 'Dirban',
    }
    return render(request, "base_dirban.html", context)


def members(request):
    context = {
        'title_head': 'Dirban - Direktori Bandung',
        'title': 'Dirban',
        'content': 'Logged in',
    }
    return render(request, "base_dirban.html", context)
