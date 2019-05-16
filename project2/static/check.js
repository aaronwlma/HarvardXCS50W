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
    // checkName(name);
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

// Check server to make sure name is not in use
// function checkName(name) {
//   // let users = {{ users }};
//   if (users.includes(name)) {
//     promptName();
//   };
// }

// function checkName(name) {
//   let users = {{ users }};
//   if (users.includes(name)) {
//     alert('Sorry, name is already in use. Please try again.');
//     document.location.reload();
//   };
// };
