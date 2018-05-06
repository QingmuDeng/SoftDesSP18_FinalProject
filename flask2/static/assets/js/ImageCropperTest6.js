var crop;

function handleFileSelect() {
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
    var bounds = crop.getCropBounds();
    document.getElementById("bounds").value = bounds.top.toString()+", "+bounds.bottom.toString()+", "+bounds.left.toString()+", "+bounds.right.toString();
    document.getElementById("img").value = document.getElementById("fileInput").src;
}

function reset() {
  document.getElementById("fileInput").hidden = true;
  document.getElementById("imageCanvas").hidden = false;
}

function drawBounds(h, w){
    // console.log("running drawBounds");
    if (document.getElementById("old_bounds").innerHTML.length > 0) {
      var result;
      result = document.getElementById("old_bounds").innerHTML.split(",");
      // console.log("testing", result);
      // console.log("testing", result[0]);
      crop.setBounds2(parseInt(result[0]), parseInt(result[1]), parseInt(result[2]), parseInt(result[3]), h, w);
    }
}
