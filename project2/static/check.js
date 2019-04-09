if (localStorage.getItem('name') == null || localStorage.getItem('name') == '') {
  promptName();
}

function promptName() {
  var name = prompt("Welcome to Flack! Please enter your name:");
  if (name == null || name == "") {
    promptName();
  } else {
    localStorage.setItem('name', name);
  };
};
