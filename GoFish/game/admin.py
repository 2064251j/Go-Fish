from django.contrib import admin
from game.models import Game, Player, Card, Plays

class PlaysInline(admin.TabularInline):
    model = Plays
    extra = 1

class GameAdmin(admin.ModelAdmin):
    inlines = (PlaysInline,)
    list_display = ('id', 'creator', 'turn', 'started', 'players', 'get_pool')

    def get_pool(self, obj):
        return "\n".join([str(p.id) for p in obj.pool.all()])

class PlayerAdmin(admin.ModelAdmin):
    inlines = (PlaysInline,)
    list_display = ('id', 'displayName')

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'suit', 'rank', 'image')

admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Card, CardAdmin)