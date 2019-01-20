var socket = io('/chat');


socket.on('count', function (data) {
  $('.user-count').html(data.count);
});

socket.on('message', function (data) {
  $('.chat').append('<b>' + data.user + '</b>: ' + data.message + '<br>');
  document.title = "New message from:" + data.user;
});

socket.on('user-list', function (data) {
  $('.users').empty();
  data.users.forEach(function(element) {
    $('.users').append('<b>' + element + '</b><br>');
  });
});

$('form').submit(function (e) {
  e.preventDefault();
  var message = $(e.target).find('input').val();
  socket.emit('message', {
    user: cookie.get('user') || 'Anonymous',
    message: message
  });

  e.target.reset();
  $(e.target).find('input').focus();
});

const chat = document.getElementById("auto-scroll")

setInterval(function() {
    const isScrolledToBottom = chat.scrollHeight - chat.clientHeight <= chat.scrollTop + 1
    chat.scrollTop = chat.scrollHeight - chat.clientHeight
}, 1000)

function format () {
  return Array.prototype.slice.call(arguments).join(' ')
}