from django.shortcuts import render
from game.forms import Name
from game.models import Game, Player

def index(request):
    context_dict = {}
    # Render the response and send it back!
    return render(request, 'game/index.html', context_dict)


def lobby(request):
    context_dict = {}
    if 'Player' in request.session:
        context_dict['Name'] = True
        player = Player.objects.get(displayName = request.session['Player'])
        context_dict['Player'] = player.displayName
        context_dict['GameID'] = player.gameLobbyID
    else:
        if request.method == 'POST':
            form = Name(request.POST)
            if form.is_valid():
                game = Game.objects.create(numOfPlayers=1)
                context_dict['GameID'] = game.gameLobbyID
                request.session['Player'] = form.cleaned_data['Name']
                player = Player.objects.create(displayName = request.session['Player'], gameLobbyID = game)
                context_dict['Name'] = True
                context_dict['Player'] = player.displayName
        else:
            form = Name()
        context_dict['form'] = form

    return render(request, 'game/lobby.html', context_dict)