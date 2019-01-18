var socket = io();

$('form').submit(function (e) {
  e.preventDefault();
  var username = $(e.target).find('input[name="username"]').val();
  var password = $(e.target).find('input[name="password"]').val();
  socket.emit('message', {
    username: username,
    password: password
  });
});

socket.on('message', function (data) {
  $('.info').append('<b>' + data.message + '<br>');
});

jQuery("input[name='mycheckbox']").each(function() {
  console.log( this.value + ":" + this.checked );
});