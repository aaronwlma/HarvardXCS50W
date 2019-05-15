// Variables to use in the script that manages what is displayed on the page
var name = localStorage.getItem('name');
var element = document.getElementById('name');
var date = new Date();
var timestamp = date.getTime();
var timestampUTC = (new Date(timestamp)).toUTCString();

// Functions defined to be used in the listeners
function promptName() {
  var name = prompt("Welcome to Flack! Please enter your name:");
  if (name == null || name == "" || name == 'null') {
    promptName();
  } else {
    localStorage.setItem('name', name);
  };
};

// Listener that dynamic adjusts page content
document.addEventListener('DOMContentLoaded', function() {
  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Logic for "login" when connecting to the server
  socket.on('connect', function() {
    if (name == null || name == '' || name == 'null') {
      promptName();
    }
    const user = name;
    socket.emit('login', user);
    element.innerHTML = 'Hi ' + user + ', welcome to Flack!';
  });

  // Logic for the "logout" button
  document.querySelectorAll('#logout').forEach(button => {
      button.onclick = () => {
          const user = name;
          socket.emit('logout', user);
          localStorage.clear('name');
          alert('Logged out!');
          document.location.reload();
      };
  });

  // Logic for message box for chat
  document.querySelector('#submit').disabled = true;
  // Enable button only if there is text in the input field
  document.querySelector('#message').onkeyup = () => {
      if (document.querySelector('#message').value.length > 0)
          document.querySelector('#submit').disabled = false;
      else
          document.querySelector('#submit').disabled = true;
  };

  // Logic for submitting a message to the server
  document.querySelector('#new-message').onsubmit = () => {

      // Create new item for list
      const li = document.createElement('li');
      li.innerHTML = "[" + timestampUTC + "] " + name + ": " + document.querySelector('#message').value;

      // Add new item to task list
      document.querySelector('#messages').append(li);

      // Clear input field and disable button again
      document.querySelector('#message').value = '';
      document.querySelector('#submit').disabled = true;

      // Stop form from submitting
      return false;
  };
});
