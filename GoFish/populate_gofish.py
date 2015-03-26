import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoFish.settings')

import django
django.setup()

from game.models import Card

def populate():

    id = 1          #Individual Card ID = 1-52
    suitId = 1      #Hearts = 1, Clubs = 2, Diamonds = 3, Spades = 4
    rankId = 1        #1-13 Ace=1, 2-10, Jack=11, Queen=12, King=13
    while id < 53:
        if suitId == 1:
            suit = "Hearts"
        elif suitId == 2:
            suit = "Clubs"
        elif suitId == 3:
            suit = "Diamonds"
        else:
            suit = "Spades"
        if rankId == 1:
            rank = "A"
        elif rankId == 11:
            rank = "J"
        elif rankId == 12:
            rank = "Q"
        elif rankId == 13:
            rank = "K"
        else:
            rank = str(rankId)
        add_card(id, suit, rank)
        id += 1
        rankId += 1
        if id%13 == 1:
            rankId = 1        #Resets rank back to 1 for each new suit. (Every 14th card)
            suitId += 1       #Increments suit every 14th card.

def add_card(cardID, suit, rank):
    c = Card.objects.get_or_create(id=cardID, suit=suit, rank=rank)[0]
    return c

if __name__ == '__main__':
    print "Starting GoFish population script..."
    populate()




