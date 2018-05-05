// function copyToClipboard(element) {
//     console.log($(element).text());
//     var $temp = $("<input>");
//     $("body").append($temp);
//     $temp.val($(element).text()).select();
//     document.execCommand("copy");
//     $temp.remove();
// }

function SelectText(element) {
    let doc = document
        , text = doc.getElementById(element)
        , range, selection
    ;
    if (doc.body.createTextRange) {
        range = document.body.createTextRange();
        range.moveToElementText(text);
        range.select();
    } else if (window.getSelection) {
        selection = window.getSelection();
        range = document.createRange();
        range.selectNodeContents(text);
        selection.removeAllRanges();
        selection.addRange(range);
    }

    return range;
}

function copyToClipboard(element) {
    console.log("hello");
    console.log(element);
    // const copyText = $(element).text();
    let copytext = SelectText(element);
    // /* Select the text field */
    // copyText.select();
    // /* Copy the text inside the text field */
    document.execCommand("copy");
}


// const span = document.querySelector("span");
//
// span.onclick = function() {
//   document.execCommand("copy");
// }
//
// span.addEventListener("copy", function(event) {
//   event.preventDefault();
//   if (event.clipboardData) {
//     event.clipboardData.setData("text/plain", span.textContent);
//     console.log(event.clipboardData.getData("text"))
//   }
// });
