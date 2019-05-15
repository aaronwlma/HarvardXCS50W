var name = localStorage.getItem('name');
var element = document.getElementById('name');

if (name == null || name == '' || name == 'null') {
  promptName();
}

function promptName() {
  var name = prompt("Welcome to Flack! Please enter your name:");
  if (name == null || name == '' || name == 'null') {
    promptName();
  } else {
    localStorage.setItem('name', name);
  };
};

document.addEventListener('DOMContentLoaded', function() {
  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Logic for "login" when connecting to the server
  socket.on('connect', function() {
    const user = name;
    if (user == null || user == '' || user == 'null') {
      element.innerHTML = '';
      promptName();
    }
    socket.emit('login', user);
    element.innerHTML = 'Hi ' + name + ', welcome to Flack!';
  });
});
