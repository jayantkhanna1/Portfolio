function change_col(id){
    for(var i=1;i<=7;i++){
        if(i!=id){ 
            document.getElementById("main"+i).style.color="white";
            
            document.getElementById("m"+i).style.color="white";
            document.getElementById("s"+i).style.color="white";
        }
        else{
            document.getElementById("main"+i).style.color="#ff014f";
            document.getElementById("m"+i).style.color="#ff014f";
            document.getElementById("s"+i).style.color="#ff014f";
        }
    }
    $("#mySidenav").fadeOut(200);
}
// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the offset position of the navbar
// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
var sticky = header.offsetTop+200;
var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  if (window.pageYOffset > sticky && !isMobile) {
      document.getElementById("header-sticky").style.visibility="visible"
   $("#header-sticky").fadeIn(500);
  } else {
    $("#header-sticky").fadeOut(100);
  }
}
//to hide nav when website is opened
$("#mySidenav").fadeOut(1);
function openNav() {
  //document.getElementById("mySidenav").style.visibility="visible"
  $("#mySidenav").fadeIn(500);
  }
  
  function closeNav() {
    $("#mySidenav").fadeOut(200);
  }