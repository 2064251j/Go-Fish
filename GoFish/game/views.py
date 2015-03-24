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
            if Player.objects.filter(playerID = request.session['Player']).exists():
                player = Player.objects.get(playerID = request.session['Player'])
            else:
                del request.session['Player']
                return redirect('/lobby')
            if Game.objects.filter(lobbyID=player.lobbyID).exists():
                return redirect('/lobby/'+str(player.lobbyID))
        key = 0
        while Game.objects.filter(lobbyID=key).exists():
            if Player.objects.filter(lobbyID=Game.objects.get(lobbyID = key)).exists():
                key = key + 1
            else:
                Game.objects.get(lobbyID=key).delete()
        game = Game.objects.create(numOfPlayers=1, lobbyID = key)
        return redirect('lobby/'+str(key))

    if 'Player' in request.session:
        context_dict['Name'] = True
        if Player.objects.filter(playerID = request.session['Player']).exists():
            player = Player.objects.get(playerID = request.session['Player'])
        else:
            del request.session['Player']
            return redirect('/lobby')

        game = Game.objects.get(lobbyID = game_id)
        if player.lobbyID != game and Game.objects.filter(lobbyID=player.lobbyID).exists():
            return redirect('/lobby/'+str(player.lobbyID))
        if game.started == True:
            return redirect('/game/'+str(player.lobbyID))
        context_dict['Player'] = player.displayName
        context_dict['GameID'] = game_id
        player.lobbyID = game
        player.save()
        users = Player.objects.filter(lobbyID=game)
        context_dict['users'] = users
        game.numOfPlayers = len(users)
        game.save()

        if game.creator == str(player.playerID):
            context_dict['creator'] = True
    else:
        if request.method == 'POST':
            form = Name(request.POST)
            if form.is_valid():
                context_dict['GameID'] = game_id
                game = Game.objects.get(lobbyID = game_id)
                name = form.cleaned_data['Name']
                key = 0
                while Player.objects.filter(playerID=key).exists():
                    key = key + 1
                player = Player.objects.create(displayName = name, lobbyID = game, playerID = key)
                if not game.creator:
                    game.creator = str(player.playerID)
                    game.save()
                request.session['Player'] = player.playerID
                context_dict['Name'] = True
                context_dict['Player'] = player.displayName
                users = Player.objects.filter(lobbyID=game)
                context_dict['users'] = users

                game.numOfPlayers = len(users)
                game.save()

                if game.creator == str(player.playerID):
                    context_dict['creator'] = True
        else:
            form = Name()
        context_dict['form'] = form

    return render(request, 'game/lobby.html', context_dict)

def game(request, game_id = None):
    context_dict = {}
    # If game doesn't exist return to lobby:
    if not Game.objects.filter(lobbyID = game_id).exists():
        return redirect('/lobby')

    # If application user is a player:
    if 'Player' in request.session:
        player = Player.objects.get(playerID = request.session['Player'])
        game = Game.objects.get(lobbyID = game_id)
        # If player not in game return to lobby:
        if player.lobbyID != game:
            return redirect('/lobby')

        # Set up the game:
        if not Pool.objects.filter(lobbyID = game).exists():    # Take a deck
            all_cards = Card.objects.all()
            pool = Pool.objects.create(lobbyID = game)
            pool.cardID = all_cards
            pool.save()
            game.started = True                                 # Start the game
            game.turn = str(Player.objects.filter(lobbyID=game)[0].playerID)
            game.save()
        else:                                                       # Already have a deck
            pool = Pool.objects.get(lobbyID = game)

        users = Player.objects.filter(lobbyID=game)             # Get users
        for user in users:
            user.score = 0                                          # Reset scores
            user.save()
            if not Hand.objects.filter(playerID = user).exists():   # Deal hands
                hand = Hand.objects.create(playerID = user)
                for i in range(5):
                    count = len(pool.cardID.all()) - 1
                    c = random.randint(0,count)
                    card = pool.cardID.all()[c]
                    hand.cardID.add(card)
                    pool.cardID.remove(card)

        hand = Hand.objects.get(playerID = player)                   # Get players hand

        # Game logics:
        plays = Player.objects.get(playerID = int(game.turn))
        if len(Hand.objects.filter(playerID = plays)) == 0:
            if len(pool) >= 5:
                for i in range(5):
                    count = len(pool.cardID.all()) - 1
                    c = random.randint(0,count)
                    card = pool.cardID.all()[c]
                    hand.cardID.add(card)
                    pool.cardID.remove(card)
            else:
                for i in range(len(pool)):
                    count = len(pool.cardID.all()) - 1
                    c = random.randint(0,count)
                    card = pool.cardID.all()[c]
                    hand.cardID.add(card)
                    pool.cardID.remove(card)

        if request.method == 'POST':
            person = request["target"]
            wanted = request["wanted"]
            if users.filter(playerID = person).exists():
                target = users.filter(playerID = person)
                crops = Hand.objects.get(playerID = target).cardID.all()
                for card in crops:
                    if card.rank == wanted:
                        Hand.objects.get(playerID = plays).cardID.add(card)
                        Hand.objects.get(playerID = target).cardID.remove(card)

        for card in Hand.objects.get(playerID = plays).cardID.all():
            count = 0
            for c in Hand.objects.get(playerID = plays).cardID.all():
                if c.rank == card.rank:
                    count = count + 1
            if count >= 4:
                for c in Hand.objects.get(playerID = plays).cardID.all():
                    if c.rank == card.rank:
                        Hand.objects.get(playerID = plays).cardID.remove(c)
                plays.score = plays.score + 1

        total = 0
        top = plays
        results = ""
        for user in users:
            total = total + user.score
            results = results + " - ".join([str(user.displayName),str(user.score)]) + " "
            if top.score < user.score:
                top = user
        if total >= 13:
            context_dict['winner'] = top
            game.delete()


        context_dict['results'] = results
        context_dict['pool'] = pool.cardID.all()
        context_dict['GameID'] = game_id
        context_dict['hand'] = hand.cardID.all()
        context_dict['Player'] = player.displayName
        context_dict['users'] = users
        context_dict['playerNumber'] = game.numOfPlayers
    else:
        return redirect('/lobby')

    return render(request, 'game/game.html', context_dict)