
// Get the current username from the cookies
var user = cookie.get('user');
if (!user) {

  // Ask for the username if there is none set already
  user = prompt('Choose a username:');
  if (!user) {
    alert('You need to specify a username');
  } else {
    // Store it in the cookies for future use
    cookie.set('user', user);
  }
}

var socket = io();

// The user count. Can change when someone joins/leaves
socket.on('count', function (data) {
  $('.user-count').html(data.count);
});

// When we receive a message
// it will be like { user: 'username', message: 'text' }
socket.on('message', function (data) {
 if ($(".chat").html().length > 5) {
    $('.chat').slice(-1,1)
 }
  $('.chat').append('<strong>' + data.user + '</strong>: ' + data.message + '<br>');
});

// When the form is submitted
$('form').submit(function (e) {
  // Avoid submitting it through HTTP
  e.preventDefault();

  // Retrieve the message from the user
  var message = $(e.target).find('input').val();

  // Send the message to the server
  socket.emit('message', {
    user: cookie.get('user') || 'Anonymous',
    message: message
  });

  // Clear the input and focus it for a new message
  e.target.reset();
  $(e.target).find('input').focus();
});

const chat = document.getElementById("chat")

setInterval(function() {
    // allow 1px inaccuracy by adding 1
    const isScrolledToBottom = chat.scrollHeight - chat.clientHeight <= chat.scrollTop + 1
    chat.scrollTop = chat.scrollHeight - chat.clientHeight

}, 1000)

function format () {
  return Array.prototype.slice.call(arguments).join(' ')
}