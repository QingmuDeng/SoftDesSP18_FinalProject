// function copyToClipboard(element) {
//     console.log($(element).text());
//     var $temp = $("<input>");
//     $("body").append($temp);
//     $temp.val($(element).text()).select();
//     document.execCommand("copy");
//     $temp.remove();
// }

function copyToClipboard(element) {
    // console.log($(element).text());
    // const copyText = $(element).text();
    // /* Select the text field */
    // copyText.select();
    // /* Copy the text inside the text field */
    // document.execCommand("Copy");

    let range, selection, worked;

    if (document.body.createTextRange) {
        range = document.body.createTextRange();
        range.moveToElementText(element);
        range.select();
      } else if (window.getSelection) {
        selection = window.getSelection();
        range = document.createRange();
        range.selectNodeContents(element);
        selection.removeAllRanges();
        selection.addRange(range);
      }

    try {
        document.execCommand('copy');
        alert('text copied');
    }
    catch (err) {
        alert('unable to copy text');
    }
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
