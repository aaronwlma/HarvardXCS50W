var name = localStorage.getItem('name');
var element = document.getElementById('name');
element.innerHTML = 'Hi ' + name + ', welcome to Flack!';

function logout() {
  localStorage.clear('name');
  alert('Logged out!');
  document.location.reload();
};

document.addEventListener('DOMContentLoaded', function() {


});
