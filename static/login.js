var socket = io();

$('form').submit(function (e) {
  e.preventDefault();
  var username = $(e.target).find('input[name="username"]').val();
  var password = $(e.target).find('input[name="password"]').val();
  cookie.set('user', username);
  socket.emit('auth', {
    username: username,
    password: password,
    session_id: cookie.get('session_id')
  });
});

socket.on('success', function (data) {
    if(data.message == "OK") {
        window.location = '/chat';
    } else {
        $('.info').append('<b>' + data.message + '<br>');
    }

});