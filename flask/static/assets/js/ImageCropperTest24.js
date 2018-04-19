/**
 * Copyright (c) 2015 Allan Bishop http://www.allanbishop.com
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 **/
/// <reference path="ImageCropper.ts"/>
var crop;
window.onload = function () {
    window.addEventListener('mouseup', preview);
    window.addEventListener('touchend', preview);
};
function preview() {
    if (crop.isImageSet()) {
        var img = crop.getCroppedImage();
        img.onload = (function () { return previewLoaded(img); });
    }
}

function to_image(){
//    <!--document.getElementById("button").style.opacity = 0;-->
    var canvas = document.getElementById("imageCanvas");
//    document.getElementById("fileInput").src = canvas.toDataURL();
//    var img = crop.getCroppedImage(600, 600);
    var bounds = String(crop.getCropBounds());
//    img.onload = (function () {
//    document.getElementById("fileInput").files[0].src = img.src;
    document.getElementById("bounds").file = bounds;
    document.getElementById("upload").submit();
}

function previewLoaded(img) {
    if (img) {
        document.getElementById("preview").appendChild(img);
    }
}

function handleFileSelect() {
//    var input = file.target;
    var img = document.createElement("IMG");
    img.setAttribute("src", document.getElementById('fileInput').src);
    img.setAttribute("width", document.getElementById('fileInput').width);
    img.setAttribute("height", document.getElementById('fileInput').height);

    // document.getElementById('fileInput').hidden = true;

    var canvas = document.getElementById("imageCanvas");
    canvas.style.opacity = 1;
    canvas.width = img.width;
    canvas.height = img.height;

    crop = new ImageCropper(canvas, canvas.width, canvas.height, img.width, img.height, true);
    crop.setImage(document.getElementById('fileInput'));
    // preview();

//    var img = new Image();
//        img.addEventListener("load", function () {
////        var maxWidth = 600;
////        var maxHeight = 600;
////        var width = img.width;
////        var height = img.height;
////        if(width > maxWidth){
////          height = Math.floor( maxWidth * height / width );
////          width = maxWidth
////          }
////
////        if(height > maxHeight){
////          width = Math.floor( maxHeight * width / height );
////          height = maxHeight;
////        }
////
////        img.width = width;
////        img.height = height;
////        img.src = img.src;
//        document.getElementById("imageCanvas").width = img.width
//        document.getElementById("imageCanvas").height = img.height
//        var canvas = document.getElementById("imageCanvas");
//        crop = new ImageCropper(canvas, canvas.width, canvas.height, width, height, true);
//        crop.setImage(img);
//        preview();
//    }, false);
//    var reader = new FileReader();
//    reader.onload = function(){
////      var dataURL = reader.result;
////      var output = document.getElementById('output');
//      img.src = reader.result;
//    };
//    reader.readAsDataURL(input.files[0]);
}

//function handleFileSelect(evt) {
//    var file = evt.target.src;
////    var file = getDataUrl(evt.currentTarget)
//    var reader = new FileReader();
//    var img = new Image();
//
//    img.addEventListener("load", function () {
//        crop.setImage(img);
//        preview();
//    }, false);
//
//    reader.addEventListener("load", function () {
//        img.src = reader.result;
//    }, false);
//    if (file) {
//        reader.readAsDataURL(file);
//    }
//}
//window.getElementById('fileInput').addEventListener('load', handleFileSelect, false);
//# sourceMappingURL=ImageCropperTest.js.map