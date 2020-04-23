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

var args = {
  min: 0,
  max: 255,
  start: 100,
  step: 10
};

// set default values
var red1 = new Powerange(red, args);
var green1 = new Powerange(green, args);
var blue1 = new Powerange(blue, args);

// handle slider value changes
function setBGColor() {
  var newColor = `rgb(${red.value}, ${green.value}, ${blue.value})`;
  document.body.style.background = newColor;
}

red0.on("mouseup", function() {
  setBGColor();
  redBox.innerHTML = red.value;
})
green0.on("mouseup", function() {
  setBGColor();
  greenBox.innerHTML = green.value;

})
blue0.on("mouseup", function() {
  setBGColor();
  blueBox.innerHTML = blue.value;
})
