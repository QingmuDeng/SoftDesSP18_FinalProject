/**
 * ImageCropper4.js acts as a connection between image.html and the library ImageCropper.js.
 * It was written by Cassandra Overney and Enmo Ren.
 **/

var crop;

function handleFileDisplay() {
    //handleFileDisplay() is called when image.html gets loaded. It creates an ImageCropper object and sets
    //the canvas' image to be the same as the uploaded image

    document.getElementById("fileInput").hidden = false;
    document.getElementById("imageCanvas").hidden = true;
    var img = document.getElementById("fileInput");
    img.crossOrigin = "Anonymous";

    var canvas = document.getElementById("imageCanvas");
    canvas.width = img.width;
    canvas.height = img.height;

    crop = new ImageCropper(canvas, img.width, img.height, img.width, img.height, true);
    crop.setImage(document.getElementById('fileInput'));
    drawBounds(img.height, img.width);
    reset();
}

function getBounds() {
    //when the user presses the "crop" button, the bounds and img source get saved in a form so it can be accessed in app.py.
    var bounds = crop.getCropBounds();
    document.getElementById("bounds").value = bounds.top.toString() + ", " + bounds.bottom.toString() + ", " + bounds.left.toString() + ", " + bounds.right.toString();
    document.getElementById("img").value = document.getElementById("fileInput").src;
}

function reset() {
    //makes the img tag hidden and displays the imageCanvas
    document.getElementById("fileInput").hidden = true;
    document.getElementById("imageCanvas").hidden = false;
}

function drawBounds(h, w) {
    //draws the previous bounds that the user selected if there are any when image.html is loaded
    if (document.getElementById("old_bounds").innerHTML.length > 0) {
        var result;
        result = document.getElementById("old_bounds").innerHTML.split(",");
        crop.setBounds2(parseInt(result[0]), parseInt(result[1]), parseInt(result[2]), parseInt(result[3]), h, w);
    }
}
