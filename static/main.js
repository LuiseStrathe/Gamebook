
/*  
    Contains all the JavaScript functions used 
  
    > Buttons
    > Navigation drop-down menu
    > Pop-up & Info Windows
    > Tabs
    > Register
    
*/





/*  ####################################

    Buttons

    #################################### */ 



// Button: Go to top

function topFunction() {
  window.scrollTo({top: 0, behavior: 'smooth'})
}


// Button: Go back to previous page

function goBack() {
  window.history.back();
}





/*  ####################################

    Navigation drop-down menu

    #################################### */ 



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function toggle_nav() {
  document.getElementById("navDrop").classList.toggle("navShow");
}


// Close the dropdown menu if the user clicks outside of it

window.onclick = function(event) {
  if (!event.target.matches('#navButton')) {
    var dropdowns = document.getElementsByClassName("navContent");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('navShow')) {
        openDropdown.classList.remove('navShow');
      }
    }
  }
}





/*  ####################################

    Pop-up & Info Windows

    #################################### */ 


// Close user INFO
function close_user_info() {
  document.getElementById("infoID").classList.remove("infoShow");
}


// Change SETTINGS confirmation

function toggle_change_settings() {
  document.getElementById("settingsID").classList.toggle("settingsShow");
}


// DELETE group confirmation

function toggle_group_delete() {
  document.getElementById("delGroupID").classList.toggle("delGroupShow");
}


// Puzzles

function puzzle_change() {
  document.getElementById("puzzleChangeForm").classList.toggle("gameShow");
}


function puzzle_add() {
  document.getElementById("puzzleAddForm").classList.toggle("gameShow");
}


function puzzle_log() {
  document.getElementById("puzzleLogForm").classList.toggle("gameShow");
}





/*  ####################################

    Tabs

    #################################### */ 


// Open the default tab

function openMode(evt, Mode) {

  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");

  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(Mode).style.display = "block";
  evt.currentTarget.className += " active";
}





/*  ####################################

    Register

    #################################### */ 



function add_player() {
  var count = document.getElementById("numberPlayers");
  var number = parseInt(count.value);
  if (number < 10) {
      number += 1;
      count.value = number;
  }
}


function remove_player() {
  var count = document.getElementById("numberPlayers");
  var number = parseInt(count.value);
  if (number > 2) {
      number -= 1;
      count.value = number;
  }
}

  
function show_players() {

  var count = document.getElementById("numberPlayers");
  var number = parseInt(count.value);

  document.getElementById("player3").classList.remove("showing");
  
  document.getElementById("player4").classList.remove("showing");
  document.getElementById("player5").classList.remove("showing");
  document.getElementById("player6").classList.remove("showing");
  document.getElementById("player7").classList.remove("showing");
  document.getElementById("player8").classList.remove("showing");
  document.getElementById("player9").classList.remove("showing");
  document.getElementById("player10").classList.remove("showing");

  if (number > 2) {
    document.getElementById("player3").classList.toggle("showing");}
    
  if (number > 3) {
    document.getElementById("player4").classList.toggle("showing");}

  if (number > 4) {
    document.getElementById("player5").classList.toggle("showing");}

  if (number > 5) {
    document.getElementById("player6").classList.toggle("showing");}

  if (number > 6) {
    document.getElementById("player7").classList.toggle("showing");}

  if (number > 7) {
    document.getElementById("player8").classList.toggle("showing");}

  if (number > 8) {
    document.getElementById("player9").classList.toggle("showing");}

  if (number > 9) {
    document.getElementById("player10").classList.toggle("showing");}
}

