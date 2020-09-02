///////////////// CROPPIE SECTION ///////////////////
let width = 40;
let height = 50;
let pixelArtEndpoint = '/api/generate_pixelart';
let source = $('#cropper-tool').croppie({
    viewport: { width: 160, height: 200 },
    boundary: { width: 400, height: 400 },
});

function readFile(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function(e) {
            source.croppie('bind', {
                url: e.target.result
            });
        }

        reader.readAsDataURL(input.files[0]);
    }
}
$('.actionUpload input').on('change', function() { readFile(this); });
$('#cropper-tool').on('update.croppie', delayedGeneration);

var timeoutHandle;
function delayedGeneration() {
    clearTimeout(timeoutHandle);
    timeoutHandle = setTimeout(generatePixelImage, 250);
}

// create the new image with the RGB color channels
function generatePixelImage() {
    redBox.innerHTML   = red.value;
    greenBox.innerHTML = green.value;
    blueBox.innerHTML  = blue.value;
    source.croppie('result', {
        type: 'base64',
        size: { 'width': width, 'height': height },
        format: 'png'
    }).then(function(foo){
        let data = foo.split(',');
        let uploadedImage = data[1];
        let mimeType = data[0].split(';')[0].split(':')[1];

        let postData = JSON.stringify({ 'image': uploadedImage });
        let queryStr =  `?red=${red.value/100}&green=${green.value/100}&blue=${blue.value/100}`;
        jQuery.post( pixelArtEndpoint + queryStr, postData, displayReturnImage);
    });
}

function displayReturnImage(returnData, textStatus, jQueryXHR){
    let srcStr = "data:image/png;base64," + returnData.image
        $('#result-img').prop('src', srcStr);
}

///////////////// POWERANGE SECTION ///////////////////
// find element
let red = document.querySelector("#red-bar .slider");
let green = document.querySelector("#green-bar .slider");
let blue = document.querySelector("#blue-bar .slider");

let red0 = $("#red-bar");
let green0 = $("#green-bar");
let blue0 = $("#blue-bar");

let redBox = document.querySelector("#red-box");
let greenBox = document.querySelector("#green-box");
let blueBox = document.querySelector("#blue-box");

let redArgs = {
    min: 80,
    max: 120,
    start: 100,
    step: 1
};

let greenArgs = Object.assign({}, redArgs);
let blueArgs =  Object.assign({}, redArgs);

// set default values
let red1 = new Powerange(red, redArgs);
let green1 = new Powerange(green, greenArgs);
let blue1 = new Powerange(blue, blueArgs);

// handle slider value changes
$(".slider-container").on("mouseup touchend", generatePixelImage);

// handle accordion collapsible content
let accordion = document.getElementsByClassName("accordion");
var i;
let panel;

for (i = 0; i < accordion.length; i++) {
    accordion[i].addEventListener("click", function() {
        let i;
        for (i = 0; i < accordion.length; i++) {
            accordion[i].classList.remove("active");
            panel = accordion[i].nextElementSibling;
            panel.style.maxHeight = null;
        }
        this.classList.add("active");
        panel = this.nextElementSibling;
        panel.style.maxHeight = panel.scrollHeight + "px";
    });
}

let step1 = $("#step1")[0];
step1.style.maxHeight = step1.scrollHeight + "px";

///////////// PRICING SECTION /////////////////
let pdfPrice   = 5;
let beadsPrice = 25;
let boardPrice = 16;
let tweezPrice = 8;
let framePrice = 5;
///////////////////////////////////////////////

$("#pdfPrice").html(pdfPrice); 
$("#beadsPrice").html(beadsPrice); 
$("#boardPrice").html(boardPrice); 
$("#tweezPrice").html(tweezPrice); 
$("#framePrice").html(framePrice); 

let boardBox = $("input[type='checkbox'][name='pegboards']");
let tweezBox = $("input[type='checkbox'][name='tweezers']");
let frameBox = $("input[type='checkbox'][name='frame']");

$('input[type=radio][name=kit]').change(getTotal);

function getTotal() {
    let total = 0;
    let radio = $("input[type='radio'][name='kit']:checked");
    if (radio.val() === 'beads') {
        total += beadsPrice;
    } else if (radio.val() === 'PDFOnly') {
        total += pdfPrice;
    }
    if (boardBox.prop('checked')) {
        total += boardPrice;
    }
    if (tweezBox.prop('checked')) {
        total += tweezPrice;
    }
    if (frameBox.prop('checked')) {
        total += framePrice;
    }

    $("#totalPrice").html(total); 
}

let orderEndpoint = '/api/submit_order';

getTotal();

// handle page submission
$("#submit").on("click", submitSelection);

function submitSelection() {
    let orderArgs = {
        image:    $("#result-img").prop('src'),
        name:     $("#name").val(),
        email:    $("#email").val(),
        phone:    $("#phone").val(),
        kit:      $("input[type='radio'][name='kit']:checked").val(),
        pegboard: boardBox.prop('checked'),
        tweezers: tweezBox.prop('checked'),
        frame:    frameBox.prop('checked'),
        total:    $("#totalPrice").html()
    }
    let postData = JSON.stringify(orderArgs);
    jQuery.post( orderEndpoint, postData, thankYou );
    return false;
}

function thankYou () {
    window.alert('You have successfully submitted your request for a Picture Bead kit. Please contact Jeff');
}
