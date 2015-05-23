from django.db import models
#from django.utils.decorators import property

class Player(models.Model):
    displayName = models.CharField(max_length=12)

    def __unicode__(self):
        return str(self.id)

class Card(models.Model):
    suit = models.CharField(max_length=10, default="")
    rank = models.CharField(max_length=1, default="")
    image = models.ImageField()

    def __unicode__(self):
        return str(self.id)

class Game(models.Model):
    creator = models.ForeignKey(Player, related_name='creator')
    turn = models.ForeignKey(Player, related_name='turn')
    players = models.ManyToManyField(Player, through='Plays')
    started = models.BooleanField(default=False)
    pool = models.ManyToManyField(Card)

    @property
    def cards_dict(self):
        dict = {}
        try:
            for card in self.pool.all():
                dict[card.id] = {"suit": card.suit, "rank": card.rank, "image": card.image}
        except:
            pass
        return dict

    def __unicode__(self):
        return str(self.id)

class Plays(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    score = models.IntegerField(default=0)
    hand = models.ManyToManyField(Card)

    @property
    def cards_dict(self):
        dict = {}
        try:
            for card in self.hand.all():
                dict[card.id] = {"suit": card.suit, "rank": card.rank, "image": card.image}
        except:
            pass
        return dict