from django.shortcuts import render, redirect
from game.forms import Name
from game.models import Game, Player

def index(request):
    context_dict = {}
    # Render the response and send it back!
    return render(request, 'game/index.html', context_dict)


def lobby(request, game_id = None):
    context_dict = {}
    if game_id == None:
        key = 0
        while Game.objects.filter(gameLobbyID=key).exists():
            key = key + 1
        game = Game.objects.create(numOfPlayers=1, gameLobbyID = key)
        return redirect('lobby/'+str(key))

    if 'Player' in request.session:
        context_dict['Name'] = True
        player = Player.objects.get(playerID = request.session['Player'])
        context_dict['Player'] = player.displayName
        context_dict['GameID'] = game_id
        game = Game.objects.get(gameLobbyID = game_id)
        player.gameLobbyID = game
        player.save()
        users = Player.objects.filter(gameLobbyID=game)
        context_dict['users'] = users
    else:
        if request.method == 'POST':
            form = Name(request.POST)
            if form.is_valid():
                context_dict['GameID'] = game_id
                game = Game.objects.get(gameLobbyID = game_id)
                name = form.cleaned_data['Name']
                key = 0
                while Player.objects.filter(playerID=key).exists():
                    key = key + 1
                player = Player.objects.create(displayName = name, gameLobbyID = game, playerID = key)
                request.session['Player'] = player.playerID
                context_dict['Name'] = True
                context_dict['Player'] = player.displayName
                users = Player.objects.filter(gameLobbyID=game)
                context_dict['users'] = users
        else:
            form = Name()
        context_dict['form'] = form

    return render(request, 'game/lobby.html', context_dict)