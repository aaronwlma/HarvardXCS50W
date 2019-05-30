// #############################################################################
// Flack - Username Verification (Client)
// #############################################################################
// @author         Aaron Ma
// @description    Chat client that allows conversations in a global chat or in
//                 custom channel
// @component      Script the client requested username against the server
//                 values
// @date           May 30th, 2019
// #############################################################################

// Retrieve what the client has as local storage values first
var name = localStorage.getItem('name');
var chat = localStorage.getItem('chat');

// Check if the local session has a name, if not, then prompt for one and verify against the server
if (name == null || name == 'null' || name == '') {
  var nameInput = prompt("Welcome to Flack! Please enter your name:");

  // Open an XMLHttpRequest to send the input to the server to validate
  const request = new XMLHttpRequest();
  request.open('POST', '/login');

  // When the server sends information to the client, run this body of code
  request.onload = function() {
    const data = JSON.parse(request.responseText);

    // If the server validation returns true, then set local storage and HTML elements to the input
    if (data.valid === true) {
      localStorage.setItem('name', nameInput);
      localStorage.setItem('chat', 'Global Chat');
      // Connect to server
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      var element = document.getElementById('name');
      element.innerHTML = 'Hi ' + nameInput + ', welcome to Flack!';
      const user = localStorage.getItem('name');
      socket.emit('initial login', user);

    }
    // If the server validation returns false, alert an invalid name and reload the page
    else {
      confirm("Name is not valid or already in use. Please try again.")
      document.location.reload();
    }
  }

  // Create and send the client data to the server
  const data = new FormData();
  data.append('nameInput', nameInput);
  request.send(data);
};
