from django.shortcuts import render


def bad_request(request, exception):
    title = '400'
    template = '400.html'
    context = {'title': title, }
    return render(request, template, context, status=400)


def permission_denied(request, exception):
    title = '403'
    template = '403.html'
    context = {'title': title, }
    return render(request, template, context, status=403)


def page_not_found(request, exception):
    title = '404'
    template = '404.html'
    context = {'title': title, }
    return render(request, template, context, status=404)


def server_error(request):
    title = '500'
    template = '500.html'
    context = {'title': title, }
    return render(request, template, context, status=500)
