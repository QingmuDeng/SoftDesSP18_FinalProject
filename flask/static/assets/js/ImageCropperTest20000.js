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
// window.onload = function () {
//     window.addEventListener('mouseup', preview);
//     window.addEventListener('touchend', preview);
// };
// function preview() {
//     if (crop.isImageSet()) {
//         var img = crop.getCroppedImage();
//         img.onload = (function () { return previewLoaded(img); });
//     }
// }

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

// function previewLoaded(img) {
//     if (img) {
//         document.getElementById("preview").appendChild(img);
//     }
// }

function handleFileSelect() {
    document.getElementById("fileInput").hidden = true;

    var img = document.getElementById("fileInput");
    img.crossOrigin = "Anonymous";

    var canvas = document.getElementById("imageCanvas");
    canvas.width = img.width;
    canvas.height = img.height;

    crop = new ImageCropper(canvas, img.width, img.height, img.width, img.height, true);
    crop.setImage(document.getElementById('fileInput'));
    drawBounds();
    // preview();
}

function getBounds() {
    var bounds = crop.getCropBounds();
    document.getElementById("bounds").value = bounds.top.toString()+", "+bounds.bottom.toString()+", "+bounds.left.toString()+", "+bounds.right.toString();
    document.getElementById("img").value = document.getElementById("fileInput").src;
}

function drawBounds(){
  console.log("HELLO");
  var result;
  result = document.getElementById("old_bounds").innerHTML.split(",");
  console.log(result);
  var bounds = Bounds(parseInt(result[0]), parseInt(result[1]), parseInt(result[2]), parseInt(result[3]));
  console.log(result[0]);
  console.log(bounds);
  crop.setBounds(bounds);
}
