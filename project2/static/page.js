// Variables to use in the script that manages what is displayed on the page
// var name = localStorage.getItem('name');
// var chat = localStorage.getItem('chat');
// var element = document.getElementById('name');
//
// // Functions defined to be used in the listeners
// function promptName() {
//   var name = prompt("Welcome to Flack! Please enter your name:");
//   if (name == null || name == "" || name == 'null') {
//     promptName();
//   } else {
//     // checkName(name);
//     var chat = 'globalChat';
//     localStorage.setItem('name', name);
//     localStorage.setItem('chat', chat);
//   };
// };

// Check server to make sure name is not in use
// function checkName(name) {
//   let users = {{ users }};
//   if (users.includes(name)) {
//     alert('Sorry, name is already in use. Please try again.');
//     document.location.reload();
//   };
// };

// Listener that dynamic adjusts page content
document.addEventListener('DOMContentLoaded', function() {
  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Logic for "login" when connecting to the server
  // socket.on('connect', function() {
  //   if (name == null || name == '' || name == 'null') {
  //     promptName();
  //   };
  //   // socket.emit('get userlist')
  //   const user = name;
  //   element.innerHTML = 'Hi ' + user + ', welcome to Flack!';
  // });

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
      // Create new item for list and submit to server
      const comment = document.createElement('li');
      comment.innerHTML = "[" + name + "]: " + document.querySelector('#message').value;
      socket.emit('submit comment', [name, chat, comment.innerHTML]);
      // Clear input field and disable button again
      document.querySelector('#message').value = '';
      document.querySelector('#submit').disabled = true;
      // Stop form from submitting
      return false;
  };

  // When a new comment is announced, add it to the unordered chat
  socket.on('announce comment', data => {
    const comment = document.createElement('li');
    comment.innerHTML = data;
    document.querySelector('#messages').append(comment);
  });

  // When the user list is announced, update the user list on the web page
  // socket.on('announce userlist', onlineUsers => {
  //   var list = '';
  //   for (const user of users) {
  //     const name = '<li>' + user + '</li>';
  //     list = list.concat(name);
  //   };
  //   document.querySelector('#online-users').innerHTML = list;
  // });

});
