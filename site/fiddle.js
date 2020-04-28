///////////////// CROPPIE SECTION ///////////////////

var basic = $('#cropper-tool').croppie({
  viewport: { width: 160, height: 200 },
  boundary: { width: 400, height: 400 },
});

function readFile(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#cropper-tool').croppie('bind', {
        url: e.target.result
      });
      $('.actionDone').toggle();
      $('.actionUpload').toggle();
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$('.actionUpload input').on('change', function() { readFile(this); });
$('.actionDone').on('click', function() {
  $('.actionDone').toggle();
  $('.actionUpload').toggle();
})

///////////////// POWERANGE SECTION ///////////////////
// find element
var red = document.querySelector("#red-bar .slider");
var green = document.querySelector("#green-bar .slider");
var blue = document.querySelector("#blue-bar .slider");

var red0 = $("#red-bar");
var green0 = $("#green-bar");
var blue0 = $("#blue-bar");

var redBox = document.querySelector("#red-box");
var greenBox = document.querySelector("#green-box");
var blueBox = document.querySelector("#blue-box");

var redArgs = {
  min: 0,
  max: 255,
  start: 40,
  step: 10
};

var greenArgs = Object.assign({}, redArgs);
greenArgs.start = 100;
var blueArgs = Object.assign({}, redArgs);
blueArgs.start = 200;

// set default values
var red1 = new Powerange(red, redArgs);
var green1 = new Powerange(green, greenArgs);
var blue1 = new Powerange(blue, blueArgs);

// handle slider value changes
function setBGColor() {
  var newColor = `rgb(${red.value}, ${green.value}, ${blue.value})`;
  document.body.style.background = newColor;
  redBox.innerHTML   = red.value;
  greenBox.innerHTML = green.value;
  blueBox.innerHTML  = blue.value;
}

var red0 = $("#red-bar");
$(".slider-container").on("mouseup", function() { setBGColor() })

setBGColor();
