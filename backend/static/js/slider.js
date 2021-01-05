var inputsRy = {
    sliderWidth: 300,
    minRange: 0,
    maxRange: 210,
    outputWidth:45, // output width
    thumbWidth: 18, // thumb width
    thumbBorderWidth: 4,
    trackHeight: 4,
    theValue: [60, 120] // theValue[0] < theValue[1]
};
var roundedLength = [0,0];
var isDragging0 = false;
var isDragging1 = false;

var range = inputsRy.maxRange - inputsRy.minRange;
var rangeK = inputsRy.sliderWidth / range;
var container = document.querySelector(".container");
var thumbRealWidth = inputsRy.thumbWidth + 2 * inputsRy.thumbBorderWidth;

// styles
var slider = document.querySelector(".slider");
slider.style.height = inputsRy.trackHeight + "px";
slider.style.width = inputsRy.sliderWidth + "px";
slider.style.paddingLeft = (inputsRy.theValue[0] - inputsRy.minRange) * rangeK + "px";
slider.style.paddingRight = inputsRy.sliderWidth - inputsRy.theValue[1] * rangeK + "px";

var track = document.querySelector(".track");
track.style.width = inputsRy.theValue[1] * rangeK - inputsRy.theValue[0] * rangeK + "px";

var thumbs = document.querySelectorAll(".thumb");
for (var i = 0; i < thumbs.length; i++) {

    thumbs[i].style.width = thumbs[i].style.height = inputsRy.thumbWidth + "px";
    console.log(inputsRy.thumbWidth + "px");
    thumbs[i].style.borderWidth = inputsRy.thumbBorderWidth + "px";
    thumbs[i].style.top = -(inputsRy.thumbWidth / 2 + inputsRy.thumbBorderWidth - inputsRy.trackHeight / 2) + "px";
    thumbs[i].style.left = (inputsRy.theValue[i] - inputsRy.minRange) * rangeK - (thumbRealWidth / 2) + "px";

}
var outputs = document.querySelectorAll(".output");
for (var i = 0; i < outputs.length; i++) {
    console.log(thumbs[i])
    outputs[i].style.width = outputs[i].style.height = outputs[i].style.lineHeight = outputs[i].style.left = inputsRy.outputWidth + "px";
    outputs[i].style.top = -(Math.sqrt(2 * inputsRy.outputWidth * inputsRy.outputWidth) + inputsRy.thumbWidth / 2 - inputsRy.trackHeight / 2) + "px";
    outputs[i].style.left = (inputsRy.theValue[i] - inputsRy.minRange) * rangeK - inputsRy.outputWidth / 2 + "px";
    outputs[i].innerHTML = "<p>" + timeConvert(inputsRy.theValue[i], i) + "</p>";
}

//events

thumbs[0].addEventListener("mousedown", function(evt) {
    isDragging0 = true;
}, false);
thumbs[1].addEventListener("mousedown", function(evt) {
    isDragging1 = true;
}, false);
container.addEventListener("mouseup", function(evt) {
    isDragging0 = false;
    isDragging1 = false;
}, false);
container.addEventListener("mouseout", function(evt) {
    isDragging0 = false;
    isDragging1 = false;
}, false);

container.addEventListener("mousemove", function(evt) {
    var mousePos = oMousePos(this, evt);
    var theValue0 = (isDragging0) ? Math.round(mousePos.x / rangeK) + inputsRy.minRange : inputsRy.theValue[0];
    console.log(theValue0);
    var theValue1 = (isDragging1) ? Math.round(mousePos.x / rangeK) + inputsRy.minRange : inputsRy.theValue[1];

    if (isDragging0) {

        if (theValue0 < theValue1 - (thumbRealWidth / 2) &&
            theValue0 >= inputsRy.minRange) {
            inputsRy.theValue[0] = theValue0;
            thumbs[0].style.left = (theValue0 - inputsRy.minRange) * rangeK - (thumbRealWidth / 2) + "px";
            outputs[0].style.left = (theValue0 - inputsRy.minRange) * rangeK - inputsRy.outputWidth / 2 + "px";
            outputs[0].innerHTML = "<p>" + timeConvert(theValue0, 0) + "</p>";
            slider.style.paddingLeft = (theValue0 - inputsRy.minRange) * rangeK + "px";
            track.style.width = (theValue1 - theValue0) * rangeK + "px";

        }
    } else if (isDragging1) {

        if (theValue1 > theValue0 + (thumbRealWidth / 2) &&
            theValue1 <= inputsRy.maxRange) {
            inputsRy.theValue[1] = theValue1;
            thumbs[1].style.left = (theValue1 - inputsRy.minRange) * rangeK - (thumbRealWidth / 2) + "px";
            outputs[1].style.left = (theValue1 - inputsRy.minRange) * rangeK - inputsRy.outputWidth / 2 + "px";
            outputs[1].innerHTML = "<p>" + timeConvert(theValue1, 1) + "</p>";
            slider.style.paddingRight = (inputsRy.maxRange - theValue1) * rangeK + "px";
            track.style.width = (theValue1 - theValue0) * rangeK + "px";

        }
    }

}, false);

// helpers

function oMousePos(elmt, evt) {
    var ClientRect = elmt.getBoundingClientRect();
    return { //objeto
        x: Math.round(evt.clientX - ClientRect.left),
        y: Math.round(evt.clientY - ClientRect.top)
    }
}


function timeConvert(n, i) {
    var num = n;
    var hours = (num / 60);
    var rhours = Math.floor(hours);
    var minutes = (hours - rhours) * 60;
    var rminutes = Math.round(minutes-minutes%5);
    roundedLength[i] = rminutes + (60*rhours);
    if (rhours < 1){
        return rminutes + "m";
    }
    if (rminutes == 0) {
        return rhours + "h";
    }
    return rhours + "h" + rminutes + "m";
}