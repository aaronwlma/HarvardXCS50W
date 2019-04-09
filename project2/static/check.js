if (localStorage.getItem('name') == null || localStorage.getItem('name') == '') {
  promptName();
}

function promptName() {
  var name = prompt("Welcome to Flack! Please enter your name:");
  if (name == null || name == "") {
    promptName();
  } else {
    // checkName(name);
    localStorage.setItem('name', name);
  };
};

function checkName(name) {
  // let users = {{ users }};
  if (users.includes(name)) {
    promptName();
  };
}
