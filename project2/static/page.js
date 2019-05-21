// Listener that dynamic adjusts page content
document.addEventListener('DOMContentLoaded', function() {
  // Connect to server
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {

    if (localStorage.getItem('chat') == null) {
      localStorage.setItem('chat', 'globalChat');
    }

    var chat = localStorage.getItem('chat')
    var name = localStorage.getItem('name')

    socket.emit('get userlist');
    socket.emit('get channel chat', chat);

    var element = document.getElementById('name');
    element.innerHTML = 'Hi ' + name + ', welcome to Flack!';

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
        socket.emit('submit comment', [name, chat, comment.innerHTML]);
        // Clear input field and disable button again
        document.querySelector('#message').value = '';
        document.querySelector('#submit').disabled = true;
        // Stop form from submitting
        return false;
    };

    // When the user list is announced, update the user list on the web page
    socket.on('announce userlist', userlist => {
      var list = '';
      for (const user of userlist) {
        const name = '<li>' + user + '</li>';
        list = list.concat(name);
      };
      document.querySelector('#online-users').innerHTML = list;
    });

    // When the the channel chat is updated, update the channel chat on the web page
    socket.on('announce channel chat', chatHistory => {
      var list = '';
      for (const chat of chatHistory) {
        const line = '<li>' + chat + '</li>';
        list = list.concat(line);
      };
      document.querySelector('#messages').innerHTML = list;
    });

  });
});
