var name = localStorage.getItem('name');
var element = document.getElementById('name');
element.innerHTML = 'Hi ' + name + ', welcome to Flack!';

document.addEventListener('DOMContentLoaded', function() {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, emit login
  socket.on('connect', function() {
    const user = name;
    socket.emit('login', user);
  });

  socket.on('announce login', addUser());

  // socket.on('announce existing', nameExists());
});

function addUser() {
  const li = document.createElement('li');
  li.innerHTML = `${user.users}`;
  document.querySelector('#online-users').append(li);
};

function logout() {
  localStorage.clear('name');
  alert('Logged out!');
  document.location.reload();
};
