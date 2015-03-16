from django.shortcuts import render

def index(request):
    context_dict = {}
    # Render the response and send it back!
    return render(request, 'game/index.html', context_dict)