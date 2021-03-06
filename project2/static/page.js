// #############################################################################
// Flack - Page Listener for Change in Events (Client)
// #############################################################################
// @author         Aaron Ma
// @description    Chat client that allows conversations in a global chat or in
//                 custom channel
// @component      Listener on the client that determines what the webpage
//                 should dynamically display for the user
// @date           May 30th, 2019
// #############################################################################

// Listener that dynamic adjusts page content
document.addEventListener('DOMContentLoaded', function() {

  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Once the socket connects, have these query selectors and socket listeners available
  socket.on('connect', () => {
    // If the client does not have a chat designated in local storage, default to the Global Chat
    if (localStorage.getItem('chat') == null) {
      localStorage.setItem('chat', 'Global Chat');
    }

    // Retrieve the local storage values for channel and username to use as variables
    var chat = localStorage.getItem('chat')
    var name = localStorage.getItem('name')

    // Each time the client connects, make sure to get the most updated user and channel lists
    socket.emit('get userlist');
    socket.emit('get channel list');
    socket.emit('get channel chat', chat);

    // Generate header elements to reflect the client's user name and channel
    var element = document.getElementById('name');
    element.innerHTML = 'Hi ' + name + ', welcome to Flack!';
    var element2 = document.getElementById('current-channel');
    element2.innerHTML = chat;

    // Logic for the HTML elements on the webpage
    // Logic for the "logout" button
    document.querySelectorAll('#logout').forEach(button => {
        button.onclick = () => {
            const user = localStorage.getItem('name');
            socket.emit('logout', user);
            localStorage.clear('name');
            alert('Logged out!');
            document.location.reload();
        };
    });

    // Logic for the "make a new channel" button
    document.querySelectorAll('#new-channel').forEach(button => {
        button.onclick = () => {
            const user = localStorage.getItem('name');
            var chanInput = prompt("Please enter a channel name:");

            // Open an XMLHttpRequest to send the input to the server to validate
            const request = new XMLHttpRequest();
            request.open('POST', '/newchan');

            // When the server sends information to the client, run this body of code
            request.onload = function() {
              const reply = JSON.parse(request.responseText);
              // If the server validation returns true, then set local storage and HTML elements to the input
              if (reply.valid === true) {
                const username = localStorage.getItem('name');
                const currchan = localStorage.getItem('chat');
                socket.emit('change channel', currchan, chanInput, username);
                localStorage.setItem('chat', chanInput);
                document.location.reload();
              }
              // If the server validation returns false, alert an invalid name and reload the page
              else {
                confirm("Name is not valid or already in use. Please try again.")
                document.location.reload();
              }
            }
            // Create and send the client data to the server
            const reply = new FormData();
            reply.append('chanInput', chanInput);
            request.send(reply);
        };
    });

    // Logic for changing channels on the server
    document.querySelector('#change-channel').onsubmit = () => {
        // Create new item for list and submit to server
        const username = localStorage.getItem('name');
        const currchan = localStorage.getItem('chat');
        const channame = document.getElementById("select-channel").value;
        socket.emit('change channel', currchan, channame, username);
        localStorage.setItem('chat', channame);
        document.location.reload();
    };

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
        const name = localStorage.getItem('name');
        const chat = localStorage.getItem('chat');
        comment.innerHTML = document.querySelector('#message').value;
        socket.emit('submit comment', name, chat, comment.innerHTML);
        // Clear input field and disable button again
        document.querySelector('#message').value = '';
        document.querySelector('#submit').disabled = true;
        // Stop form from submitting
        return false;
    };

    // Listeners for when the server broadcasts a message
    // When the user list is announced, update the user list on the web page
    socket.on('announce userlist', userlist => {
      var list = '';
      for (const user of userlist) {
        const name = '<li>' + user + '</li>';
        list = list.concat(name);
      };
      document.querySelector('#channel-users').innerHTML = list;
    });

    // When the channel list is announced, update the user list on the web page
    socket.on('announce channel list', channellist => {
      var list = '';

      for (const channel of channellist) {
        const channame = '<li>' + channel + '</li>';
        list = list.concat(channame);
      };
    });

    // When the the channel chat is updated, update the channel chat on the web page
    socket.on('announce channel chat', chatHistory => {
      var list = '';
      if (localStorage.getItem('chat') == chatHistory[1]) {
        for (const chat of chatHistory[0]) {
          const line = '<li>' + chat + '</li>';
          list = list.concat(line);
        };
        document.querySelector('#messages').innerHTML = list;
      };
      var textarea = document.getElementById('messages');
      textarea.scrollTop = textarea.scrollHeight;
    });
  });
});
