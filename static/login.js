var socket = io();

$('form').submit(function (e) {
  e.preventDefault();
  var message = $(e.target).find('input').val();
  socket.emit('message', {
    message: message
  });
});

socket.on('message', function (data) {
  $('.info').append('<b>' data.message + '</b>');
});