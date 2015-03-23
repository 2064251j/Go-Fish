import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoFish.settings')

import django
django.setup()

from game.models import Game, Player, Card, Hand, Pool
