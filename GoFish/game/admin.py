from django.contrib import admin
from game.models import Game, Player, Card, Hand, Pool

class GameAdmin(admin.ModelAdmin):
    list_display = ('gameLobbyID', 'numOfPlayers', 'gameCreator', 'gameStarted' )

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('gameLobbyID', 'score', 'playerID', 'displayName')

class CardAdmin(admin.ModelAdmin):
    list_display = ('cardID', 'suit', 'rank')

class HandAdmin(admin.ModelAdmin):
    list_display = ('playerID', 'get_cards')

    def get_cards(self, obj):
        return "\n".join([str(p.cardID) for p in obj.cardID.all()])

class PoolAdmin(admin.ModelAdmin):
    list_display = ('gameLobbyID','get_cards')

    def get_cards(self, obj):
        return ", \n".join([str(p.cardID) for p in obj.cardID.all()])

admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Hand, HandAdmin)
admin.site.register(Pool, PoolAdmin)