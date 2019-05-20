// var name = localStorage.getItem('name');
// var chat = localStorage.getItem('chat');

if (localStorage.getItem('name') === null) {
  var nameInput = prompt("Welcome to Flack! Please enter your name:");

  if (nameInput != null || nameInput != '' || nameInput != 'null') {
    // Connect to server
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.emit('login', nameInput);

    socket.on('announce userlist', userlist => {
      localStorage.setItem('name', nameInput);
      var element = document.getElementById('name');
      element.innerHTML = 'Hi ' + nameInput + ', welcome to Flack!';
    });

    socket.on('fail validation', nameInput => {
      document.location.reload();
    });
  }
  else {
    document.location.reload();
  };
}
else {
  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.emit('login', nameInput);

  socket.on('announce userlist', userlist => {
    localStorage.setItem('name', nameInput);
    var element = document.getElementById('name');
    element.innerHTML = 'Hi ' + nameInput + ', welcome to Flack!';
  });
};


// function promptName() {
//   var name = prompt("Welcome to Flack! Please enter your name:");
//   if (name == null || name == '' || name == 'null') {
//     promptName();
//   } else {
//     var chat = 'globalChat';
//     localStorage.setItem('name', name);
//     localStorage.setItem('chat', chat);
//   };
// };

// document.addEventListener('DOMContentLoaded', function() {
//   // Connect to server
//   var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
//
//   // Logic for "login" when connecting to the server
//   socket.on('connect', function() {
//     const user = name;
//     if (user == null || user == '' || user == 'null') {
//       element.innerHTML = '';
//       promptName();
//     }
//     socket.emit('login', user);
//     element.innerHTML = 'Hi ' + name + ', welcome to Flack!';
//   });
// });
