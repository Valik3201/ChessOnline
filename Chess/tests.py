from django.test import TestCase
from django.test.client import Client
from django.core.cache import cache
from Chess.models import *
from time import sleep


class TestGameCreating(TestCase):
    def setUp(self):
        self.client1 = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client2 = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.user1 = User.objects.create(username='username1', password='password')
        self.user2 = User.objects.create(username='username2', password='password')




    def test_index_view(self):
        c = self.client1
        response = c.get('/')
        self.assertEqual(response.status_code, 200)



    def test_crating_game(self):
        player1 = {'id': self.user1.id, 'rating': self.user1.rating}
        player2 = {'id': self.user2.id, 'rating': self.user2.rating}
        players=[player1,player2]
        cache.set("players",players)
        sleep(5)
        games=cache.get("games")
        self.assertEqual(games[0]["id"], self.user1.id)

    def test_deleting_game(self):
        games=cache.get("games")
        if games:
            games[0]["status"] = "finished"
            cache.set('games', games)
            sleep(2)
            self.assertFalse(cache.get("games"))
            self.assertFalse(cache.get("players_in_game"))
    def test_delete_from_search(self):
        player2 = {'id': self.user2.id, 'rating': self.user2.rating}
        player1 = {'id': self.user1.id, 'rating': self.user1.rating}
        players=[player1,player2]
        cache.set("players",players)
        cache.set("players_in_game",players)
        sleep(4)
        self.assertEqual(cache.get("players"), [])
    










