function copyToClipboard(element) {
    console.log($(element).text());
    var textarea = document.createElement('textarea');
    textarea.textContent = $(element).text();
    document.body.appendChild(textarea);
    var selection = document.getSelection();
    var range = document.createRange();
    range.selectNode(textarea);
    selection.removeAllRanges();
    selection.addRange(range);
    console.log('copy success', document.execCommand('copy'));
    selection.removeAllRanges();
    document.body.removeChild(textarea);
}
