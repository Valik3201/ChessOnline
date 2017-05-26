from channels.routing import route

from Chess.consumers import ws_receive# ws_connect

channel_routing = [
    route("websocket.receive", ws_receive, ),
      #route("websocket.connect", ws_connect,),
]