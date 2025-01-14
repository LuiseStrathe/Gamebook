
// Navigation drop-down menu


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function toggle_nav() {
  document.getElementById("navDrop").classList.toggle("show");
}


// Close the dropdown menu if the user clicks outside of it

window.onclick = function(event) {
  if (!event.target.matches('#navButton')) {
    var dropdowns = document.getElementsByClassName("navContent");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}




// Button: Go to top

function topFunction() {
  window.scrollTo({top: 0, behavior: 'smooth'})
}


// Button: Go back to previous page

function goBack() {
  window.history.back();
}