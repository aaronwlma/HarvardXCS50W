chooseName()

function chooseName() {
  var person = prompt("Welcome to Flack! Please enter a display name:", "");
  if (person == null || person == "") {
    chooseName();
  }
  else {
    txt = "Hello " + person + "! How are you today?";
  }
}
