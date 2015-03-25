from django.db import models
#from django.utils.decorators import property

class Game(models.Model):
    lobbyID = models.CharField(max_length=128, unique=True)
    numOfPlayers = models.IntegerField(default=0)
    creator = models.TextField(null=True)
    turn = models.TextField(null=True)
    started = models.BooleanField(default=False)

    def __unicode__(self):
        return self.lobbyID

class Player(models.Model):
    lobbyID = models.ForeignKey(Game)
    score = models.IntegerField(default=0)
    playerID = models.CharField(max_length=128, unique=True)
    displayName = models.CharField(max_length=12)

    def __unicode__(self):
        return self.playerID

class Card(models.Model):
    cardID = models.IntegerField(max_length=2)
    suit = models.CharField(max_length=10, default="")
    rank = models.CharField(max_length=1, default="")

    def __unicode__(self):
        return unicode(self.cardID)

class Hand(models.Model):
    playerID = models.ForeignKey(Player)
    cardID = models.ManyToManyField(Card)

    @property
    def cards_dict(self):
        dict = {}
        try:
            for card in self.cardID.all():
                dict[card.cardID] = {"suit": card.suit, "rank": card.rank}
        except:
            pass
        return dict

    def __unicode__(self):
        return unicode(self.playerID)

class Pool(models.Model):
    lobbyID = models.ForeignKey(Game)
    cardID = models.ManyToManyField(Card)

    @property
    def cards_dict(self):
        dict = {}
        try:
            for card in self.cardID.all():
                dict[card.cardID] = {"suit": card.suit, "rank": card.rank}
        except:
            pass
        return dict

    def __unicode__(self):
        return unicode(self.lobbyID)