var socket = new WebSocket('ws://' + window.location.host );
var game_id=0,color,turn,game_status;
var text = document.getElementsByTagName("input")[0];
var id = text.value;
// do not pick up pieces if the game is over
// only pick up pieces for the side to move

var board,
  game = new Chess(),
  statusEl = $('#status'),
  fenEl = $('#fen'),
  pgnEl = $('#pgn');

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
var onDragStart = function(source, piece, position, orientation) {
  if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};
 waitForSocketConnection(socket, function () {


      var text = document.getElementsByTagName("input")[0];
      var id = text.value;
      var info={"game_status":"start","user_id":id};
      var data=JSON.stringify(info);
      socket.send(data);
  });



socket.onmessage=function (msg) {
    console.log('got message ', msg);
    data = JSON.parse(msg.data);
    if (data["game_status"]=="start") {
        color = data["color"];

        game_id = data["game_id"];
        turn = data["turn"];
        board.orientation(color);
        updateStatus();

    }
    if (data["game_id"]==-1) {

        game_status=data["game_status"];
        game_id = data["game_id"];
        turn = data["turn"];
        board.orientation(color);
        updateStatus();

    }

    if (data["game_status"] == "move") {
        var moveObj = ({
          from: data["source"],
          to: data["target"],
          promotion: 'q' // NOTE: always promote to a queen for example simplicity
        });

            var move = game.move(moveObj);
            // illegal move

            if (move === null) {
                return;
            }

            turn = data["turn"];

    updateStatus();
    board.position(game.fen());

    }
};

var onDrop = function(source, target) {
  // see if the move is legal
    if(game_id>0){
       if (turn==color) {


           waitForSocketConnection(socket, function () {


               var info = {"game_status": "move", "game_id": game_id, "turn": turn, "source": source, "target": target};
               var data = JSON.stringify(info);
               socket.send(data);

            // illegal move
           });
       }



   }



  // illegal move



};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
  board.position(game.fen());
};

var updateStatus = function() {
  var status = '';

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // checkmate?
  if (game.in_checkmate() === true) {
       if(color=="white"){
                if(turn=="white") {
                    var winner = "black";
                }
                else{
                    var winner="white";
                }

                waitForSocketConnection(socket, function () {


                    var info = {"game_status": "finished", "white": id, "winner": winner, "game_id": game_id};
                    var data = JSON.stringify(info);
                    socket.send(data);

                    // illegal move
                });


        }
    status = 'Game over, ' + moveColor + ' is in checkmate.';
  }

  // draw?
  else if (game.in_draw() === true) {
       if(color=="white"){

                var win = "draw";

                waitForSocketConnection(socket, function () {


                    var info = {"game_status": "finished", "white": id, "winner": win, "game_id": game_id};
                    var data = JSON.stringify(info);
                    socket.send(data);

                    // illegal move
                });


        }

    status = 'Game over, drawn position';
  }

  // game still on
  else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
    }
  }
if(!game_id){
      status="Wait for 2'nd player";
}
if(game_id==-1){
      status=game_status;
}
  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());
};

var cfg = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};
board = ChessBoard('board', cfg);

updateStatus();





//
function waitForSocketConnection(socket, callback){
      setTimeout(
          function () {
              if (socket.readyState === 1) {
                  console.log("Connection is made")
                  if(callback != null){
                      callback();
                  }
                  return;

              } else {
                  console.log("wait for connection...")
                  waitForSocketConnection(socket, callback);
              }

          }, 50); // wait 5 milisecond for the connection...
  }