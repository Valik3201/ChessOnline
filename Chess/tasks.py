from celery.task import periodic_task
from datetime import timedelta
from django.core.cache import cache
from random import randint




@periodic_task(run_every = timedelta(seconds = 2))
def clear_search():
    if not cache.get("search_lock"):
        cache.set("search_lock",True)
        s_players=cache.get('players')
        g_players=cache.get('players_in_game')
        if s_players and g_players:
            for player in s_players:
                if player in g_players: s_players.remove(player)
            cache.set('players',s_players)
        cache.set("search_lock",False)

@periodic_task(run_every = timedelta(seconds = 1))
def clear_game_list():
        games=cache.get('games')
        players_in_game=cache.get('players_in_game')
        if games:
            for game in games:
                if game['status']=='finished':
                    if players_in_game:
                        if game['p1'] in players_in_game: players_in_game.remove(game['p1'])
                        if game['p2'] in players_in_game: players_in_game.remove(game['p2'])
                    games.remove(game)
            cache.set('games',games)
            cache.set('players_in_game',players_in_game)




def get_pair(players):
    for player1 in players:
        min=[10000,1,2]
        players.remove(player1)
        for player2 in players:
            if abs(player1['rating']-player2['rating'])<min[0]:
                min[0]=abs(player1['rating']-player2['rating'])
                min[1]=player1
                min[2]=player2
        if cache.get('players_in_game'):
            in_game=cache.get('players_in_game')
            if not min[1] in in_game:
                in_game.apend(min[1])
            if not min[2] in in_game:
                in_game.apend(min[2])
            cache.set('players_in_game', in_game)
        else:
            plrs = [min[1], min[2]]
            cache.set('players_in_game',plrs)
        yield (min[1],min[2])


@periodic_task(run_every = timedelta(seconds = 4))
def create_games():
    players=cache.get('players')
    if players:
        if len(players)>1:
            if len(players)%2==0:
                pairs=get_pair(players)
            else:
                pairs=get_pair((players[1:]))
            for pair in pairs:
                color=randint(1,2)
                if color==1: white=pair[1]['id']
                else: white=pair[0]['id']
                if (cache.get('game')):
                    games=cache.get('games')
                    game={'id':min(pair[0]['id'],pair[1]['id']),'p1':pair[0],'p2':pair[1],
                          'status':'not finished','white':white}
                    if not game in games:
                        games.append(game)
                        cache.set('games',games,10)
                else:
                    game = {'id': min(pair[0]['id'], pair[1]['id']), 'p1': pair[0], 'p2': pair[1],
                            'status': 'not finished','white':white}
                    games=[game,]
                    cache.set('games', games)
        else: return players
