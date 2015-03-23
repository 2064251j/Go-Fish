import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoFish.settings')

import django
django.setup()

from game.models import Player, Card

def populate():

    id = 1          #Individual Card ID = 1-52
    suit = 1        #Hearts = 1, Clubs = 2, Diamonds = 3, Spades = 4
    rank = 1        #1-13 Ace=1, 2-10, Jack=11, Queen=12, King=13
    while id < 53:
        add_card(id, suit, rank)
        id += 1
        rank += 1
        if id%13 == 1:
            rank = 1        #Resets rank back to 1 for each new suit. (Every 14th card)
            suit += 1       #Increments suit every 14th card.

def add_card(cardID, suit, rank):
    c = Card.objects.get_or_create(cardID=cardID, suit=suit, rank=rank)[0]
    return c

if __name__ == '__main__':
    print "Starting GoFish population script..."
    populate()




