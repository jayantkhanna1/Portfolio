// Changes string in home   
consoleText(['Jayant Khanna','Django-developer','Ethical Hacker', 'AR Developer']);

function consoleText(words, id, colors) {
  if (colors === undefined) colors = ['#fff'];
  var visible = true;
  var con = document.getElementById('console');
  var letterCount = 1;
  var x = 1;
  var waiting = false;
  var target = document.getElementById('console')
  window.setInterval(function() {

    if (letterCount === 0 && waiting === false) {
      waiting = true;
      target.innerHTML = words[0].substring(0, letterCount)
      window.setTimeout(function() {
        var usedColor = colors.shift();
        colors.push(usedColor);
        var usedWord = words.shift();
        words.push(usedWord);
        x = 1;
        letterCount += x;
        waiting = false;
      }, 0)
    } else if (letterCount === words[0].length + 1 && waiting === false) {
      waiting = true;
      window.setTimeout(function() {
        x = -1;
        letterCount += x;
        waiting = false;
      }, 3000)
    } else if (waiting === false) {
      target.innerHTML = words[0].substring(0, letterCount)
      letterCount += x;
    }
  }, 10)
  window.setInterval(function() {
    if (visible === true) {
      con.className = 'console-underscore hidden'
      visible = false;

    } else {
      con.className = 'console-underscore'

      visible = true;
    }
  }, 400)
}
var years=new Date().getFullYear()-2020;
document.getElementById("years").innerHTML=years;

function change_col_res_head(id){
  for(var i=1;i<=4;i++){
    if(i!=id){
      document.getElementById("r"+i).style.color="white"
      document.getElementById("r"+i).style.boxShadow="none"
      document.getElementById("r"+i).style.background="none"
      $(".res"+i).fadeOut(12)
    }
    else{
      document.getElementById("r"+i).style.width="100%"
      document.getElementById("r"+i).style.color="#fe1f4f"
      document.getElementById("r"+i).style.boxShadow="10px 10px 19px #1c1e22, -10px -10px 19px #262a2e"
      document.getElementById("r"+i).style.background="linear-gradient(145deg, #1e2024, #23272b)"
      $(".res"+i).fadeIn(600)
    }
  }
}
function change_price_col(id)
{
  for(var i=1;i<=3;i++){
    if(i!=id){
      document.getElementById("p"+i).style.color="white"
      document.getElementById("p"+i).style.boxShadow="none"
      document.getElementById("p"+i).style.background="none"
      $("#pricing-"+i).fadeOut(12)
    }
    else{
      document.getElementById("p"+i).style.width="100%"
      document.getElementById("p"+i).style.color="#fe1f4f"
      document.getElementById("p"+i).style.boxShadow="10px 10px 19px #1c1e22, -10px -10px 19px #262a2e"
      document.getElementById("p"+i).style.background="linear-gradient(145deg, #1e2024, #23272b)"
      $("#pricing-"+i).fadeIn(600)
    }
  }
}
function check_form(){
  username=document.getElementById("name").value;
  subject=document.getElementById("subject").value;
  message=document.getElementById("message").value;
  number=document.getElementById("number").value;
  email=document.getElementById("email-form").value;
  if(username=='')
  {
    document.getElementById("error").innerHTML="*ENTER NAME!";
    document.getElementById("error").style.display="block";
    return false;
  }
  else if(number=='')
  {
    document.getElementById("error").innerHTML="*ENTER NUMBER!";
    document.getElementById("error").style.display="block";
    return false;
  }
  else if(email=='')
  {
    document.getElementById("error").innerHTML="*ENTER EMAIL!";
    document.getElementById("error").style.display="block";
    return false;
  }
  else if(subject=='')
  {
    document.getElementById("error").innerHTML="*ENTER SUBJECT!";
    document.getElementById("error").style.display="block";
    return false;
  }
  else if(message=='')
  {
    document.getElementById("error").innerHTML="*ENTER MESSAGE!";
    document.getElementById("error").style.display="block";
    return false;
  }
  
}
function insta(){
  window.open('https://www.instagram.com/jayant_khanna1/','_blank')
}
function github(){
  window.open('https://github.com/jayantkhanna1','_blank')
}
function linkedln(){
  window.open('https://www.linkedin.com/in/jayant-khanna-66a274185/','_blank')
}


// flickity

var $carousel = $('.carousel').flickity({
  imagesLoaded: true,
  percentPosition: false,
});

var $imgs = $carousel.find('.carousel-cell img');
// get transform property
var docStyle = document.documentElement.style;
var transformProp = typeof docStyle.transform == 'string' ?
  'transform' : 'WebkitTransform';
// get Flickity instance
var flkty = $carousel.data('flickity');

$carousel.on( 'scroll.flickity', function() {
  flkty.slides.forEach( function( slide, i ) {
    var img = $imgs[i];
    var x = ( slide.target + flkty.x ) * -1/3;
    img.style[ transformProp ] = 'translateX(' + x  + 'px)';
  });
});
