from django.shortcuts import render, redirect
from game.forms import Name
from game.models import Game, Player, Hand, Pool, Card
from django.http import HttpResponse
import random
import json

def index(request):
    context_dict = {}
    # Render the response and send it back!
    return render(request, 'game/index.html', context_dict)

def ready(request):
    if request.is_ajax():
        gId = request.POST['id']
        string = ""
        if Game.objects.filter(id = gId).exists():
            game = Game.objects.get(id = gId)
            users = Player.objects.filter(lobbyID=game)
            player = Player.objects.get(id = request.session['Player'])
            for user in users:
                string += "<tr>"
                if user == player:
                    string += "<td class = \"info\" >" + str(user.displayName) + "</td>"
                else:
                    string = string + "<td>" + str(user.displayName) + "</td>"
                string += "<tr>"
            if Game.objects.get(id = gId).started:
                return HttpResponse('<button onclick="location.href=\'/game/'+gId+'/\'" class="btn btn-default">Join the game!</button>;'+string)
            else:
                if int(game.creator) == player.id:
                    return HttpResponse(';'+string)
    return HttpResponse('Waiting...;'+string)

def ready2(request):
    if request.is_ajax():
        player = Player.objects.get(id = request.session['Player'])
        hand = Hand.objects.get(playerID = player).cardID.all()
        game = player.lobbyID
        if int(game.turn) == player.id:
            string = "True;"
        else:
            string = "False;"

        for card in hand:
            string += "<div class=\"radio\"> <label>" \
                      "<input type=\"radio\" name=\"wanted\" id="+str(card.rank)+" value="+str(card.rank)+" checked>"\
                      +str(card.rank)+" "+str(card.suit)+"</label></div>"
        return HttpResponse(string)
    return HttpResponse('Waiting...')



def lobby(request, game_id = None):
    context_dict = {}

    # If there is no such a game:
    if game_id == None:
        # If player has a session:
        if 'Player' in request.session:
            # If player in database:
            if Player.objects.filter(id = request.session['Player']).exists():
                player = Player.objects.get(id = request.session['Player'])
            # Else delete session and reload:
            else:
                del request.session['Player']
                return redirect('/lobby')
            # If player still in the game, redirect him there:
            return redirect('/lobby/'+str(player.lobbyID))
        key = 0
        while Game.objects.filter(id=key).exists():
            if Player.objects.filter(lobbyID=Game.objects.get(id = key)).exists():
                key = key + 1
            else:
                Game.objects.get(id=key).delete()
        Game.objects.create(id=key)
        return redirect('lobby/'+str(key))

    if 'Player' in request.session:
        context_dict['Name'] = True
        if Player.objects.filter(id = request.session['Player']).exists():
            player = Player.objects.get(id = request.session['Player'])
        else:
            del request.session['Player']
            return redirect('/lobby')

        game = Game.objects.get(id = game_id)
        if player.lobbyID != game:
            return redirect('/lobby/'+str(player.lobbyID))
        if game.started == True:
            return redirect('/game/'+str(player.lobbyID))
        context_dict['Player'] = player
        context_dict['GameID'] = game_id
        player.lobbyID = game
        player.save()
        users = Player.objects.filter(lobbyID = game)
        context_dict['users'] = users
        game.numOfPlayers = len(users)
        game.save()

        if game.creator == str(player.id):
            context_dict['creator'] = True
    else:
        if request.method == 'POST':
            form = Name(request.POST)
            if form.is_valid():
                context_dict['GameID'] = game_id
                game = Game.objects.get(id = game_id)
                name = form.cleaned_data['Name']
                key = 0
                while Player.objects.filter(id=key).exists():
                    key = key + 1
                player = Player.objects.create(displayName = name, lobbyID = game, id=key)
                if not game.creator:
                    game.creator = str(player.id)
                    game.save()
                request.session['Player'] = player.id
                context_dict['Name'] = True
                context_dict['Player'] = player
                users = Player.objects.filter(lobbyID = game)
                context_dict['users'] = users

                game.numOfPlayers = len(users)
                game.save()

                if game.creator == str(player.id):
                    context_dict['creator'] = True
        else:
            form = Name()
        context_dict['form'] = form

    return render(request, 'game/lobby.html', context_dict)

def game(request, game_id = None):
    context_dict = {}
    # If game doesn't exist return to lobby:
    if not Game.objects.filter(id = game_id).exists():
        return redirect('/lobby')

    # If application user is a player:
    if 'Player' in request.session:
        player = Player.objects.get(id = request.session['Player'])
        game = Game.objects.get(id = game_id)
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
            game.turn = str(Player.objects.filter(lobbyID = game)[0].id)
            game.save()
        else:                                                       # Already have a deck
            pool = Pool.objects.get(lobbyID = game)

        users = Player.objects.filter(lobbyID = game)             # Get users
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

        context_dict['pool'] = pool.cardID.all()
        context_dict['GameID'] = game_id
        context_dict['hand'] = hand.cardID.all()
        context_dict['Player'] = player
        context_dict['users'] = users
        context_dict['playerNumber'] = game.numOfPlayers
    else:
        return redirect('/lobby')

    return render(request, 'game/game.html', context_dict)

def create_post(request):
    if request.method == 'POST':
        target = request.POST.get('target')
        wanted = request.POST.get('wanted')
        response_data = {}

        if 'Player' in request.session:
            player = Player.objects.get(id = request.session['Player'])
            game = player.lobbyID
            hand = Hand.objects.get(playerID = player)
            users = Player.objects.filter(lobbyID = game)
            for i in range(len(users)):
                if (users[i] == player):
                    if i < (len(users)-1):
                        game.turn = str(users[i+1].id)
                        game.save()
                    else:
                        game.turn = str(users[0].id)
                        game.save()

            who = Player.objects.get(id = target)
            hand2 = Hand.objects.get(playerID = who)
            pool = Pool.objects.get(lobbyID = game)
            fish = True
            for card in hand2.cardID.all():
                if card.rank == wanted:
                    fish = False
                    hand.cardID.add(card)
                    hand2.cardID.remove(card)
            if fish:
                count = len(pool.cardID.all()) - 1
                c = random.randint(0,count)
                card = pool.cardID.all()[c]
                hand.cardID.add(card)
                pool.cardID.remove(card)

            for card in hand.cardID.all():
                count = 0
                for c in hand.cardID.all():
                    if c.rank == card.rank:
                        count = count + 1
                if count == 4:
                    player.score = player.score + player.score
                    player.save()
                    for c in hand.cardID.all():
                        if c.rank == card.rank:
                            hand.cardID.remove(c)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )