if (localStorage.getItem('name') == null || localStorage.getItem('name') == '') {
  promptName();
}

function promptName() {
  var name = prompt("Welcome to Flack! Please enter your name:");
  if (name == null || name == "") {
    promptName();
  };
  localStorage.setItem('name', name);
  var element = document.getElementById('name');
  element.innerHTML = name;
};

function logout() {
  localStorage.clear('name');
  alert('Cleared local storage');
}


// document.addEventListener('DOMContentLoaded', function() {
//
//
// });
