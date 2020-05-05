///////////////// CROPPIE SECTION ///////////////////
var width = 40;
var height = 50;
var apiURL = 'http://localhost:8000/generate_pixelart';
var source = $('#cropper-tool').croppie({
  viewport: { width: 160, height: 200 },
  boundary: { width: 400, height: 400 },
});

function readFile(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      source.croppie('bind', {
        url: e.target.result
      });
    }

    reader.readAsDataURL(input.files[0]);
  }
}
$('.actionUpload input').on('change', function() { readFile(this); });
$('.actionDone').on('click', generatePixelImage);
       
// create the new image with the RGB color channels
function generatePixelImage() {
    // $('.actionDone').toggle();
    // $('.actionUpload').toggle();
    source.croppie('result', {
        type: 'base64',
        size: { 'width': width, 'height': height },
        format: 'png'
    }).then(function(foo){
        var data = foo.split(',');
        var uploadedImage = data[1];
        var mimeType = data[0].split(';')[0].split(':')[1];

        var postData = JSON.stringify({ 'image': uploadedImage });
        var queryStr =  `?red=${red.value/100}&green=${green.value/100}&blue=${blue.value/100}`;
        jQuery.post( apiURL + queryStr, postData, displayReturnImage);
    });
}

function displayReturnImage(returnData, textStatus, jQueryXHR){
    var srcStr = "data:image/png;base64," + returnData.image
    $('#result-img').attr('src', srcStr);
}

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
  min: 80,
  max: 120,
  start: 100,
  step: 1
};

var greenArgs = Object.assign({}, redArgs);
var blueArgs =  Object.assign({}, redArgs);

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
  generatePixelImage();
}

var red0 = $("#red-bar");
$(".slider-container").on("mouseup", setBGColor);

setBGColor();
