from django.shortcuts import render, redirect
from game.forms import Name
from game.models import Game, Player, Hand, Pool, Card
import random

def index(request):
    context_dict = {}
    # Render the response and send it back!
    return render(request, 'game/index.html', context_dict)


def lobby(request, game_id = None):
    context_dict = {}
    # If there is no such a game:
    if game_id == None:
        # If player is in different game
        if 'Player' in request.session:
            player = Player.objects.get(playerID = request.session['Player'])
            if Game.objects.filter(gameLobbyID=player.gameLobbyID).exists():
                return redirect('/lobby/'+str(player.gameLobbyID))
        key = 0
        while Game.objects.filter(gameLobbyID=key).exists():
            if Player.objects.filter(gameLobbyID=Game.objects.get(gameLobbyID = key)).exists():
                key = key + 1
            else:
                Game.objects.get(gameLobbyID=key).delete()
        game = Game.objects.create(numOfPlayers=1, gameLobbyID = key)
        return redirect('lobby/'+str(key))

    if 'Player' in request.session:
        context_dict['Name'] = True
        if Player.objects.filter(playerID = request.session['Player']).exists():
            player = Player.objects.get(playerID = request.session['Player'])
        else:
            del request.session['Player']
            return redirect('/lobby')

        game = Game.objects.get(gameLobbyID = game_id)
        if player.gameLobbyID != game and Game.objects.filter(gameLobbyID=player.gameLobbyID).exists():
            return redirect('/lobby/'+str(player.gameLobbyID))
        if game.gameStarted == True:
            return redirect('/game/'+str(player.gameLobbyID))
        context_dict['Player'] = player.displayName
        context_dict['GameID'] = game_id
        player.gameLobbyID = game
        player.save()
        users = Player.objects.filter(gameLobbyID=game)
        context_dict['users'] = users
        game.numOfPlayers = len(users)
        game.save()

        if game.gameCreator == str(player.playerID):
            context_dict['creator'] = True
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
                if not game.gameCreator:
                    game.gameCreator = str(player.playerID)
                    game.save()
                request.session['Player'] = player.playerID
                context_dict['Name'] = True
                context_dict['Player'] = player.displayName
                users = Player.objects.filter(gameLobbyID=game)
                context_dict['users'] = users

                game.numOfPlayers = len(users)
                game.save()

                if game.gameCreator == str(player.playerID):
                    context_dict['creator'] = True
        else:
            form = Name()
        context_dict['form'] = form

    return render(request, 'game/lobby.html', context_dict)

def game(request, game_id = None):
    context_dict = {}
    # If game doesn't exist return to lobby:
    if not Game.objects.filter(gameLobbyID = game_id).exists():
        return redirect('/lobby')

    # If application user is a player:
    if 'Player' in request.session:
        player = Player.objects.get(playerID = request.session['Player'])
        game = Game.objects.get(gameLobbyID = game_id)
        # If player not in game return to lobby:
        if player.gameLobbyID != game:
            return redirect('/lobby')

        # Set up the game:
        if not Pool.objects.filter(gameLobbyID = game).exists():
            all_cards = Card.objects.all()
            pool = Pool.objects.create(gameLobbyID = game)
            pool.cardID = all_cards
            pool.save()
            game.gameStarted = True
            game.save()
            player.score = 0
            player.save()
        else:
            pool = Pool.objects.get(gameLobbyID = game)

        users = Player.objects.filter(gameLobbyID=game)
        if not Hand.objects.filter(playerID = player).exists():
            hand = Hand.objects.create(playerID = player)
            for i in range(5):
                count = len(pool.cardID.all()) - 1
                c = random.randint(0,count)
                card = pool.cardID.all()[c]
                hand.cardID.add(card)
                pool.cardID.remove(card)
        else:
            hand = Hand.objects.get(playerID = player)

        # Game logics:
  #      for i in range(len(users)):
   #         if len(Hand.objects.filter(playerID = users[i])) == 0:
    #            if len(pool) >= 5:



        context_dict['pool'] = pool.cardID.all()
        context_dict['GameID'] = game_id
        context_dict['hand'] = hand.cardID.all()
        context_dict['Player'] = player.displayName
        context_dict['users'] = users
        context_dict['playerNumber'] = game.numOfPlayers
    else:
        return redirect('/lobby')

    return render(request, 'game/game.html', context_dict)