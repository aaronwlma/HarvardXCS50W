chooseName()

function chooseName() {
  var person = prompt("Please enter your name:", "");
  if (person == null || person == "") {
    chooseName();
  }
  else {
    txt = "Hello " + person + "! How are you today?";
  }
}
