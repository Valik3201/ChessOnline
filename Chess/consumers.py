import json
from django.core.cache import cache
from channels.channel import Group
from channels.sessions import channel_session
from time import sleep
from .models import Game,User
from datetime import datetime

def save_game(win_color,w_player,game_id,iteration=1):
    if iteration==10: return

    game=find_game(user_id=int(game_id))
    new_game=Game()
    if game['p1']['id']==int(w_player):
        w_player=game['p1']
        b_player=game['p2']
    else:
        w_player=game['p2']
        b_player=game['p1']
    new_game.black_player=b_player['id']
    new_game.white_player=w_player['id']
    new_game.win_color=win_color
    new_game.date=datetime.now()
    b_user = User.objects.get(id=b_player['id'])
    w_user = User.objects.get(id=w_player['id'])
    if win_color=="white":
        w_user.victorys+=1
        b_user.defeats+=1
    elif win_color=="black":
        b_user.victorys += 1
        w_user.defeats += 1
    else:
        b_user.draws += 1
        w_user.draws += 1
    w_user.save()
    b_user.save()


    new_game.save()

    if not cache.get("game_lock"):
        cache.set("game_lock",True)
        games=cache.get("games")
        games.remove(game)
        game['status']="finished"
        games.append(game)
        cache.set("games",games)
        cache.set("game_lock",False)
    else:
        sleep(2)
        save_game(win_color,w_player['id'],game_id,iteration=iteration+1)

def _save_game(win_color,white_player,game_id,):

    game=find_game(game_id)
    new_game=Game()
    new_game.win_color=win_color
    if game['p1']==white_player:
        black_user=game['p2']
    else: black_player=game["p1"]
    new_game.black_player=black_player
    new_game.white_player=black_player
    new_game.save()
    if not cache.get("game_lock"):
        cache.set("game_lock",True)
        games=cache.get("games")
        games.remove(game)
        game['status']="finished"
        games.append(game)
        cache.set("games",games)
        cache.set("game_lock",False)
    else:
        save_game(win_color,white_player,game_id)


def find_game(user_id,turn_id=1):
    games=cache.get('games')
    if games:
        for game in games:
            if game['p1']['id']==user_id or game['p2']['id']==user_id:
                return game
            else:
                if turn_id == 10: return None
                sleep(2)
                return find_game(user_id,turn_id=turn_id+1)
    else:
        if turn_id == 10: return None
        sleep(2)
        return find_game(user_id,turn_id=turn_id+1)



@channel_session
def ws_receive(message):
   try:
       data = json.loads(message['text'])
       if data['game_status']=='start':
           game=find_game(int(data['user_id']))
           if game:
               Group(str(game['id'])).add(message.reply_channel)
               p1=game['p1']
               p2=game['p2']
               if game['white']==int(data['user_id']):
                   color='white'
               else:
                   color='black'
               resp={'game_id':game['id'],'color':color,'turn':'white','game_status':'start'}
               j_resp = json.dumps(resp)
               message.reply_channel.send({
                   "text": j_resp,
               })
           else:
               resp={'game_id':-1,'color':"white",
                     "game_status":"There no players searching for a game. Try a bit later"}
               j_resp = json.dumps(resp)
               message.reply_channel.send({
                   "text": j_resp,
               })

       elif data['game_status']=='move':
           if data["turn"]=='white':
               turn='black'
           else: turn='white'
           #turn='white'
           resp={"game_status":"move",'game_id':data['game_id'],'turn':turn,'source':data['source'],'target':data['target']}
           j_resp=json.dumps(resp)
           Group(str(data['game_id'])).send({
               "text": j_resp
           })
       elif data['game_status']=='finished':
           print("Error")
           winner=data["winner"]
           white=data["white"]
           game_id=data["game_id"]
           save_game(winner,white,game_id)



   except ValueError:
       message.reply_channel.send({
           "text": json.dumps({
               "Error": "ValueError",
               "reply_channel": message.reply_channel.name,
           })
       })


"""
def ws_receive(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
   message.reply_channel.send({
           "text": message.content['text'],
       })
"""