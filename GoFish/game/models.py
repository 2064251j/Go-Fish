from django.db import models

class Game(models.Model):
    gameLobbyID = models.CharField(max_length=128, unique=True)
    numOfPlayers = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.gameLobbyID

class Player(models.Model):
    gameLobbyID = models.ForeignKey(Game)
    playerID = models.CharField(max_length=128, unique=True)
    displayName = models.CharField(max_length=12)

    def __unicode__(self):
        return self.playerID

class Card(models.Model):
    cardID = models.IntegerField(max_length=2)

    def __unicode__(self):
        return self.cardID

class Hand(models.Model):
    playerID = models.ForeignKey(Player)
    cardID = models.ManyToManyField(Card)

    def __unicode__(self):
        return self.cardID

class Pool(models.Model):
    cardID = models.ManyToManyField(Card)

    def __unicode__(self):
        return self.cardID